from tkinter import ttk
from db import connect_db

class BrigadeTypesTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.setup_tab()

    def setup_tab(self):
        """Настройка вкладки."""
        label = ttk.Label(self.frame, text="Список видов бригад:")
        label.pack(pady=10)

        # Таблица для отображения данных
        self.brigade_tree = ttk.Treeview(
            self.frame, 
            columns=("ID", "Название", "Описание"),
            show="headings"
        )
        self.brigade_tree.heading("ID", text="ID")
        self.brigade_tree.heading("Название", text="Название")
        self.brigade_tree.heading("Описание", text="Описание")
        self.brigade_tree.pack(expand=True, fill="both", padx=10, pady=10)

    def load_brigade_types(self):
        """Загружает данные о видах бригад из базы данных."""
        # Очистка таблицы
        for item in self.brigade_tree.get_children():
            self.brigade_tree.delete(item)

        # Подключение к базе и получение данных
        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, name, description FROM brigade_types")
            brigade_types = cursor.fetchall()

            # Добавляем данные в таблицу
            for brigade in brigade_types:
                self.brigade_tree.insert("", "end", values=brigade)
        except Exception as e:
            print(f"Ошибка загрузки данных: {e}")
        finally:
            conn.close()

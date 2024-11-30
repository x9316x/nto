from tkinter import ttk
from db import connect_db

class WorkshopsTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        parent.add(self.frame, text="Цеха завода")
        self.setup_tab()

    def setup_tab(self):
        """Настраивает вкладку."""
        ttk.Label(self.frame, text="Список цехов завода").pack(pady=10)

        # Таблица для отображения цехов
        self.tree = ttk.Treeview(self.frame, columns=("ID", "Name"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Название")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        # Загрузка данных
        self.load_workshops()

    def load_workshops(self):
        """Загружает данные о цехах завода из базы."""
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM workshops")
        rows = cursor.fetchall()
        conn.close()

        # Очищаем таблицу перед загрузкой
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Заполняем таблицу данными
        for row in rows:
            self.tree.insert("", "end", values=row)

from tkinter import ttk, Label, Entry, Button, messagebox
from db import connect_db
import datetime


class CalendarTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        parent.add(self.frame, text="Календарь рабочих смен")
        self.setup_tab()

    def setup_tab(self):
        """Настраивает вкладку."""
        # Заголовок
        Label(self.frame, text="Календарь рабочих смен").pack(pady=10)

        # Поле для выбора даты
        Label(self.frame, text="Выберите дату (YYYY-MM-DD):").pack(pady=5)
        self.date_entry = Entry(self.frame)
        self.date_entry.pack(pady=5, padx=10, fill="x")

        # Кнопка для загрузки данных
        Button(self.frame, text="Показать свободные участки", command=self.load_free_sections).pack(pady=10)

        # Таблица для отображения свободных участков
        self.sections_tree = ttk.Treeview(
            self.frame,
            columns=("ID", "Name", "Description"),
            show="headings"
        )
        self.sections_tree.heading("ID", text="ID")
        self.sections_tree.heading("Name", text="Название участка")
        self.sections_tree.heading("Description", text="Описание")
        self.sections_tree.pack(expand=True, fill="both", padx=10, pady=10)

    def load_free_sections(self):
        """Загружает список свободных участков на выбранную дату."""
        selected_date = self.date_entry.get().strip()
        try:
            # Проверка формата даты
            datetime.datetime.strptime(selected_date, "%Y-%m-%d")

            # Получение свободных участков
            free_sections = self.get_free_sections(selected_date)

            # Очищаем таблицу перед загрузкой
            for item in self.sections_tree.get_children():
                self.sections_tree.delete(item)

            # Заполняем таблицу данными
            if free_sections:
                for section in free_sections:
                    self.sections_tree.insert("", "end", values=section)
            else:
                messagebox.showinfo("Результат", "На выбранную дату нет свободных участков.")
        except ValueError:
            messagebox.showerror("Ошибка", "Введите дату в формате YYYY-MM-DD.")

    @staticmethod
    def get_free_sections(date):
        """Получает список свободных участков на указанную дату."""
        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT s.id, s.name, s.description
                FROM sections s
                WHERE s.id NOT IN (
                    SELECT section_id
                    FROM section_availability
                    WHERE date = ?
                )
            """, (date,))
            return cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")
            return []
        finally:
            conn.close()

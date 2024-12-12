from tkinter import ttk
from db import connect_db

class EmployeesTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.setup_tab()

    def setup_tab(self):
        """Настройка вкладки."""
        label = ttk.Label(self.frame, text="Список сотрудников:")
        label.pack(pady=10)

        # Таблица для отображения данных
        self.employees_tree = ttk.Treeview(
            self.frame, 
            columns=("ID", "ФИО", "Год рождения"),
            show="headings"
        )
        self.employees_tree.heading("ID", text="ID")
        self.employees_tree.heading("ФИО", text="ФИО")
        self.employees_tree.heading("Год рождения", text="Год рождения")
        self.employees_tree.pack(expand=True, fill="both", padx=10, pady=10)

    def load_employees(self):
        """Загружает данные о сотрудниках из базы данных."""
        # Очистка таблицы
        for item in self.employees_tree.get_children():
            self.employees_tree.delete(item)

        # Подключение к базе и получение данных
        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, full_name, birth_year FROM employees")
            employees = cursor.fetchall()

            # Добавляем данные в таблицу
            for employee in employees:
                self.employees_tree.insert("", "end", values=employee)
        except Exception as e:
            print(f"Ошибка загрузки данных: {e}")
        finally:
            conn.close()

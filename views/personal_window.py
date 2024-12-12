import tkinter as tk
from tkinter import ttk
from views.tabs.brigade_types_tab import BrigadeTypesTab
from views.tabs.employees_tab import EmployeesTab
from views.tabs.schedule_registration_tab import ScheduleRegistrationTab  # Импортируем новую вкладку
from views.tabs.brigade_schedule_tab import BrigadeScheduleTab

class PersonalServiceWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Персонал")
        self.window.geometry("600x400")

        # Создаем вкладки
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(expand=True, fill=tk.BOTH)

        # Подключаем вкладки
        self.brigade_types_tab = BrigadeTypesTab(self.notebook)
        self.notebook.add(self.brigade_types_tab.frame, text="Виды бригад")

        self.employees_tab = EmployeesTab(self.notebook)
        self.notebook.add(self.employees_tab.frame, text="Сотрудники")

        self.schedule_registration_tab = ScheduleRegistrationTab(self.notebook)  # Подключаем вкладку регистрации расписания
        self.notebook.add(self.schedule_registration_tab.frame, text="Регистрация расписания")

        # Добавляем вкладку расписания
        self.brigade_schedule_tab = BrigadeScheduleTab(self.notebook)
        self.notebook.add(self.brigade_schedule_tab.frame, text="Календарь работы бригад")

        # Привязка события смены вкладки
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

    def on_tab_change(self, event):
        """Обработчик смены вкладки, обновляет данные в зависимости от активной вкладки."""
        selected_tab = self.notebook.select()  # Получаем ID текущей вкладки
        current_tab = self.notebook.nametowidget(selected_tab)  # Получаем виджет текущей вкладки

        # Проверяем текущую вкладку и вызываем метод обновления данных
        if current_tab == self.brigade_types_tab.frame:
            self.brigade_types_tab.load_brigade_types()  # Загружаем данные для вкладки "Виды бригад"
        elif current_tab == self.employees_tab.frame:
            self.employees_tab.load_employees()  # Загружаем данные для вкладки "Сотрудники"
        elif current_tab == self.schedule_registration_tab.frame:
            self.schedule_registration_tab.load_schedules()  # Загружаем данные для вкладки "Регистрация расписания"

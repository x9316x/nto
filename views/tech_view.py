from tkinter import ttk, Toplevel
from views.tabs.products_tab import ProductsTab
from views.tabs.workshops_tab import WorkshopsTab  # Импортируем вкладку "Цеха завода"
from views.tabs.sections_tab import SectionsTab  # Импортируем вкладку "Участки"
from views.tabs.preparation_tasks_tab import PreparationTasksTab  # Импортируем вкладку "Задания на подготовку"
from views.tabs.desktop_tab import DesktopTab  # Импортируем вкладку "Рабочий стол"
from views.tabs.shift_tasks_tab import ShiftTasksTab  # Импортируем вкладку "Задания на смену"

class TechServiceWindow:
    def __init__(self, parent):
        self.window = Toplevel(parent)
        self.window.title("Служба технолога")
        self.window.geometry("600x400")

        # Создаём вкладки
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(expand=True, fill="both")

        # Вкладка "Виды лесопродукции"
        self.products_tab = ProductsTab(self.notebook)  # Полный функционал через ProductsTab
        self.notebook.add(self.products_tab.frame, text="Виды лесопродукции")

        # Вкладка "Цеха завода"
        self.workshops_tab = WorkshopsTab(self.notebook)  # Полный функционал через WorkshopsTab
        self.notebook.add(self.workshops_tab.frame, text="Цеха завода")

        # Вкладка "Участки"
        self.sections_tab = SectionsTab(self.notebook)  # Полный функционал через SectionsTab
        self.notebook.add(self.sections_tab.frame, text="Участки")

        # Вкладка "Задания на подготовку/оснастку"
        self.preparation_tasks_tab = PreparationTasksTab(self.notebook)  # Полный функционал через PreparationTasksTab
        self.notebook.add(self.preparation_tasks_tab.frame, text="Задания на подготовку")

        # Вкладка "Рабочий стол"
        self.desktop_tab = DesktopTab(self.notebook)  # Полный функционал через DesktopTab
        self.notebook.add(self.desktop_tab.frame, text="Рабочий стол")

        # Вкладка "Задания на смену"
        self.shift_tasks_tab = ShiftTasksTab(self.notebook)  # Полный функционал через ShiftTasksTab
        self.notebook.add(self.shift_tasks_tab.frame, text="Задания на смену")

        # Привязка события смены вкладки
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

    def on_tab_change(self, event):
        """Обработчик смены вкладки, обновляет данные на текущей вкладке."""
        selected_tab = self.notebook.select()  # Получаем ID текущей вкладки
        current_tab = self.notebook.nametowidget(selected_tab)  # Получаем виджет текущей вкладки

        # Проверяем текущую вкладку и вызываем метод обновления данных
        if current_tab == self.products_tab.frame:
            self.products_tab.load_products()  # Загружаем данные для вкладки "Виды лесопродукции"
        elif current_tab == self.workshops_tab.frame:
            self.workshops_tab.load_workshops()  # Загружаем данные для вкладки "Цеха завода"
        elif current_tab == self.sections_tab.frame:
            self.sections_tab.load_sections()  # Загружаем данные для вкладки "Участки"
        elif current_tab == self.preparation_tasks_tab.frame:
            self.preparation_tasks_tab.load_preparation_tasks()  # Загружаем данные для вкладки "Задания на подготовку"
        elif current_tab == self.desktop_tab.frame:
            self.desktop_tab.load_tasks()  # Загружаем данные для вкладки "Рабочий стол"
        elif current_tab == self.shift_tasks_tab.frame:
            self.shift_tasks_tab.load_production_tasks()  # Загружаем данные для вкладки "Задания на смену"
        elif current_tab == self.shift_tasks_tab.frame:
            self.shift_tasks_tab.load_shift_tasks()  # Загружаем данные для вкладки "Задания на смену"

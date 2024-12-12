from tkinter import ttk, Toplevel
from views.tabs.products_tab import ProductsTab
from views.tabs.orders_tab import OrdersTab
from views.tabs.workshops_tab import WorkshopsTab
from views.tabs.sections_tab import SectionsTab
from views.tabs.production_tasks_tab import ProductionTasksTab
from views.tabs.shift_tasks_tab import ShiftTasksTab  # Импортируем вкладку "Задания на смену"

class ProductionServiceWindow:
    def __init__(self, parent):
        self.window = Toplevel(parent)
        self.window.title("Служба производства")
        self.window.geometry("600x400")

        # Создаём вкладки
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(expand=True, fill="both")

        # Вкладка "Виды лесопродукции"
        self.products_tab = ProductsTab(self.notebook)
        self.notebook.add(self.products_tab.frame, text="Виды лесопродукции")

        # Вкладка "Заказы"
        self.orders_tab = OrdersTab(self.notebook)
        self.notebook.add(self.orders_tab.frame, text="Заказы")

        # Вкладка "Цеха завода"
        self.workshops_tab = WorkshopsTab(self.notebook)
        self.notebook.add(self.workshops_tab.frame, text="Цеха завода")

        # Вкладка "Участки"
        self.sections_tab = SectionsTab(self.notebook)
        self.notebook.add(self.sections_tab.frame, text="Участки")

        # Вкладка "Задания на производство"
        self.production_tasks_tab = ProductionTasksTab(self.notebook)
        self.notebook.add(self.production_tasks_tab.frame, text="Задания на производство")

        # Вкладка "Задания на смену"
        self.shift_tasks_tab = ShiftTasksTab(self.notebook)  # Полный функционал через ShiftTasksTab
        self.notebook.add(self.shift_tasks_tab.frame, text="Задания на смену")

        # Привязка события смены вкладки
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

    def on_tab_changed(self, event):
        """Обработчик смены вкладки, обновляет данные на текущей вкладке."""
        selected_tab = self.notebook.select()  # Получаем ID текущей вкладки
        current_tab = self.notebook.nametowidget(selected_tab)  # Получаем виджет текущей вкладки

        # Проверяем вкладку и вызываем соответствующий метод загрузки данных
        if current_tab == self.products_tab.frame:
            self.products_tab.load_products()  # Загружаем данные для вкладки "Виды лесопродукции"
        elif current_tab == self.orders_tab.frame:
            self.orders_tab.load_orders()  # Загружаем данные для вкладки "Заказы"
        elif current_tab == self.workshops_tab.frame:
            self.workshops_tab.load_workshops()  # Загружаем данные для вкладки "Цеха завода"
        elif current_tab == self.sections_tab.frame:
            self.sections_tab.load_sections()  # Загружаем данные для вкладки "Участки"
        elif current_tab == self.production_tasks_tab.frame:
            self.production_tasks_tab.load_orders()  # Загружаем заказы для вкладки "Задания на производство"
            self.production_tasks_tab.load_tasks()  # Загружаем задания для вкладки "Задания на производство"
        elif current_tab == self.shift_tasks_tab.frame:
            self.shift_tasks_tab.load_production_tasks()  # Загружаем данные для вкладки "Задания на смену"
        elif current_tab == self.shift_tasks_tab.frame:
            self.shift_tasks_tab.load_shift_tasks()  # Загружаем данные для вкладки "Задания на смену"        
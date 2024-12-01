from tkinter import ttk, Toplevel, messagebox
from tkinter import StringVar, IntVar
from db import connect_db
from views.tabs.products_tab import ProductsTab
from views.tabs.orders_tab import OrdersTab
from views.tabs.workshops_tab import WorkshopsTab  # Импортируем вкладку "Цеха завода"
from views.tabs.sections_tab import SectionsTab  # Импортируем вкладку "Участки"
from views.tabs.production_tasks_tab import ProductionTasksTab  # Импортируем вкладку "Задания на производство"

class ProductionServiceWindow:
    def __init__(self, parent):
        self.window = Toplevel(parent)
        self.window.title("Служба производства")
        self.window.geometry("600x400")

        # Создаём вкладки
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(expand=True, fill="both")

        # Вкладка "Виды лесопродукции"
        self.products_tab = ProductsTab(self.notebook)  # Полный функционал через ProductsTab

        # Вкладка "Заказы"
        self.orders_tab = OrdersTab(self.notebook)  # Полный функционал через OrdersTab

        # Вкладка "Цеха завода"
        self.workshops_tab = WorkshopsTab(self.notebook)  # Полный функционал через WorkshopsTab

        # Вкладка "Участки"
        self.sections_tab = SectionsTab(self.notebook)  # Полный функционал через SectionsTab

        # Вкладка "Задания на производство"
        self.production_tasks_tab = ProductionTasksTab(self.notebook)  # Полный функционал через ProductionTasksTab

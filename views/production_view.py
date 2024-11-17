from tkinter import ttk, Toplevel, messagebox
from tkinter import StringVar, IntVar
from db import connect_db
from views.tabs.products_tab import ProductsTab
from views.tabs.orders_tab import OrdersTab

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

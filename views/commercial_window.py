import tkinter as tk
from tkinter import ttk
from views.tabs.products_tab import ProductsTab
from views.tabs.clients_tab import ClientsTab
from views.tabs.orders_tab import OrdersTab

class CommercialServiceWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Коммерческая служба")
        self.window.geometry("600x400")

        # Создаём вкладки
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(expand=True, fill=tk.BOTH)

        # Подключаем вкладки
        self.products_tab = ProductsTab(self.notebook)
        self.clients_tab = ClientsTab(self.notebook)
        self.orders_tab = OrdersTab(self.notebook)

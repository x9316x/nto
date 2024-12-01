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
        self.notebook.add(self.products_tab.frame, text="Продукция")

        self.clients_tab = ClientsTab(self.notebook)
        self.notebook.add(self.clients_tab.frame, text="Клиенты")

        self.orders_tab = OrdersTab(self.notebook)
        self.notebook.add(self.orders_tab.frame, text="Заказы")

        # Привязка события смены вкладки
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

    def on_tab_change(self, event):
        """Обработчик смены вкладки, обновляет данные в зависимости от активной вкладки."""
        selected_tab = self.notebook.select()  # Получаем ID текущей вкладки
        current_tab = self.notebook.nametowidget(selected_tab)  # Получаем виджет текущей вкладки

        # Проверяем текущую вкладку и вызываем метод обновления данных
        if current_tab == self.products_tab.frame:
            self.products_tab.load_products()  # Загружаем данные для вкладки "Продукция"
        elif current_tab == self.clients_tab.frame:
            self.clients_tab.load_clients()  # Загружаем данные для вкладки "Клиенты"
        elif current_tab == self.orders_tab.frame:
            self.orders_tab.load_orders()  # Загружаем данные для вкладки "Заказы"

from tkinter import ttk, Toplevel
from views.tabs.products_tab import ProductsTab

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

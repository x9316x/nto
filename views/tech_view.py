from tkinter import ttk, Toplevel
from views.tabs.products_tab import ProductsTab
from views.tabs.workshops_tab import WorkshopsTab  # Импортируем вкладку "Цеха завода"
from views.tabs.sections_tab import SectionsTab  # Импортируем вкладку "Участки"

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

        # Вкладка "Цеха завода"
        self.workshops_tab = WorkshopsTab(self.notebook)  # Полный функционал через WorkshopsTab

        # Вкладка "Участки"
        self.sections_tab = SectionsTab(self.notebook)  # Полный функционал через SectionsTab

import tkinter as tk
from tkinter import ttk
from db import connect_db  # Подключаем базу данных

class CommercialServiceWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Коммерческая служба")
        self.window.geometry("600x400")

        # Создаем вкладки
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(expand=True, fill=tk.BOTH)

        # Вкладка "Виды лесопродукции"
        self.products_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.products_tab, text="Виды лесопродукции")
        self.setup_products_tab()

        # Вкладка "Клиенты"
        self.clients_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.clients_tab, text="Клиенты")
        self.setup_clients_tab()

        # Вкладка "Заказы"
        self.orders_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.orders_tab, text="Заказы")
        self.setup_orders_tab()

    def setup_products_tab(self):
        """Настраивает вкладку для видов лесопродукции."""
        ttk.Label(self.products_tab, text="Список видов лесопродукции").pack(pady=10)

        # Таблица
        self.products_tree = ttk.Treeview(self.products_tab, columns=("ID", "Name"), show="headings")
        self.products_tree.heading("ID", text="ID")
        self.products_tree.heading("Name", text="Название")
        self.products_tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Загружаем данные
        self.load_products()

    def setup_clients_tab(self):
        """Настраивает вкладку для клиентов."""
        ttk.Label(self.clients_tab, text="Список клиентов").pack(pady=10)

        # Таблица
        self.clients_tree = ttk.Treeview(self.clients_tab, columns=("ID", "Contact", "Phone", "Email"), show="headings")
        self.clients_tree.heading("ID", text="ID")
        self.clients_tree.heading("Contact", text="Контактное лицо")
        self.clients_tree.heading("Phone", text="Телефон")
        self.clients_tree.heading("Email", text="Email")
        self.clients_tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Загружаем данные
        self.load_clients()

    def setup_orders_tab(self):
        """Настраивает вкладку для заказов."""
        ttk.Label(self.orders_tab, text="Список заказов").pack(pady=10)

        # Таблица
        self.orders_tree = ttk.Treeview(self.orders_tab, columns=("ID", "Order Date", "Due Date", "Client", "Product", "Quantity", "Status"), show="headings")
        self.orders_tree.heading("ID", text="ID")
        self.orders_tree.heading("Order Date", text="Дата регистрации")
        self.orders_tree.heading("Due Date", text="Дата выполнения")
        self.orders_tree.heading("Client", text="Клиент")
        self.orders_tree.heading("Product", text="Продукт")
        self.orders_tree.heading("Quantity", text="Количество")
        self.orders_tree.heading("Status", text="Статус")
        self.orders_tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Загружаем данные
        self.load_orders()

    def load_products(self):
        """Загружает данные о видах лесопродукции из базы."""
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM products")
        rows = cursor.fetchall()
        conn.close()

        # Очищаем таблицу перед загрузкой
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)

        # Заполняем таблицу
        for row in rows:
            self.products_tree.insert("", "end", values=row)

    def load_clients(self):
        """Загружает данные о клиентах из базы."""
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, contact_person, phone, email FROM clients")
        rows = cursor.fetchall()
        conn.close()

        # Очищаем таблицу перед загрузкой
        for item in self.clients_tree.get_children():
            self.clients_tree.delete(item)

        # Заполняем таблицу
        for row in rows:
            self.clients_tree.insert("", "end", values=row)

    def load_orders(self):
        """Загружает данные о заказах из базы."""
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT o.id, o.order_date, o.due_date, c.contact_person, p.name, o.quantity, s.status_name
            FROM orders o
            JOIN clients c ON o.client_id = c.id
            JOIN products p ON o.product_id = p.id
            JOIN order_status s ON o.status_id = s.id
        """)
        rows = cursor.fetchall()
        conn.close()

        # Очищаем таблицу перед загрузкой
        for item in self.orders_tree.get_children():
            self.orders_tree.delete(item)

        # Заполняем таблицу
        for row in rows:
            self.orders_tree.insert("", "end", values=row)
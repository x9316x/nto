import sqlite3
import os
import sys

def resource_path(relative_path):
    """Возвращает путь к ресурсам (например, базе данных)."""
    if hasattr(sys, '_MEIPASS'):
        # Если запускается собранное приложение (.exe)
        return os.path.join(sys._MEIPASS, relative_path)
    else:
        # Если приложение запускается как .py
        return os.path.join(os.path.abspath("."), relative_path)

def get_writable_db_path():
    """Возвращает путь к базе данных, которая хранится рядом с приложением."""
    base_path = os.path.abspath(os.path.join(".", "database", "sawmill.db"))
    os.makedirs(os.path.dirname(base_path), exist_ok=True)
    return base_path

def connect_db():
    """Создает подключение к базе данных."""
    writable_db_path = get_writable_db_path()
    print("Путь к базе данных:", writable_db_path)  # Для отладки
    return sqlite3.connect(writable_db_path)

def create_tables():
    """Создает таблицы, если их ещё нет."""
    conn = connect_db()
    cursor = conn.cursor()

    # Таблица "Виды лесопродукции"
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)

    # Таблица "Клиенты завода"
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contact_person TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)

    # Таблица "Статусы заказа"
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            status_name TEXT NOT NULL
        )
    """)

    # Таблица "Заказы"
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_date TEXT NOT NULL,
            due_date TEXT,
            client_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            additional_info TEXT,
            status_id INTEGER NOT NULL,
            FOREIGN KEY (client_id) REFERENCES clients(id),
            FOREIGN KEY (product_id) REFERENCES products(id),
            FOREIGN KEY (status_id) REFERENCES order_status(id)
        )
    """)

    # Таблица "Цеха завода"
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS workshops (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)

    # Таблица "Участки цеха"
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            workshop_id INTEGER NOT NULL,
            description TEXT,
            FOREIGN KEY (workshop_id) REFERENCES workshops(id)
        )
    """)

    # Таблица "Задания на производство"
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS production_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            registration_date TEXT NOT NULL,
            start_date TEXT NOT NULL,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            workshops TEXT NOT NULL,
            additional_info TEXT,
            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)

    # Новая таблица "Задания на подготовку/оснастку"
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS preparation_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            registration_date TEXT NOT NULL,
            required_date TEXT NOT NULL,
            production_task_id INTEGER NOT NULL,
            section_id INTEGER NOT NULL,
            additional_info TEXT,
            status TEXT NOT NULL DEFAULT 'Создано',
            FOREIGN KEY (production_task_id) REFERENCES production_tasks(id),
            FOREIGN KEY (section_id) REFERENCES sections(id)
        )
    """)

    conn.commit()
    conn.close()

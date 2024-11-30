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

    # Новая таблица "Цеха завода"
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS workshops (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

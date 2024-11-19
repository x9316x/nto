import sqlite3
import os
import sys
import shutil

def resource_path(relative_path):
    """Возвращает путь к ресурсам (например, базе данных)."""
    if hasattr(sys, '_MEIPASS'):
        # Если запускается собранное приложение (.exe)
        return os.path.join(sys._MEIPASS, relative_path)
    else:
        # Если приложение запускается как .py
        return os.path.join(os.path.abspath("."), relative_path)

def get_writable_db_path():
    """Возвращает путь к базе данных, доступный для записи."""
    # Папка пользователя
    user_folder = os.path.expanduser("~")
    app_folder = os.path.join(user_folder, "MyApp")  # Папка для вашего приложения
    os.makedirs(app_folder, exist_ok=True)  # Создаём папку, если её нет

    db_path = os.path.join(app_folder, "sawmill.db")  # Путь к базе в папке пользователя

    # Копируем базу данных, если её там ещё нет
    if not os.path.exists(db_path):
        original_db_path = resource_path("database/sawmill.db")
        shutil.copyfile(original_db_path, db_path)

    return db_path

def connect_db():
    """Создает подключение к базе данных."""
    writable_db_path = get_writable_db_path()
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
            due_date TEXT NOT NULL,
            client_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            additional_info TEXT,
            status_id INTEGER NOT NULL,
            FOREIGN KEY (client_id) REFERENCES clients(id),
            FOREIGN KEY (product_id) REFERENCES products(id),
            FOREIGN KEY (status_id) REFERENCES order_status(id)
        )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    print("Таблицы созданы успешно!")

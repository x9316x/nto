import sqlite3
import os

# Путь к базе данных
DB_PATH = "database/sawmill.db"

# Создание папки для базы данных, если её нет
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def connect_db():
    """Создает подключение к базе данных."""
    return sqlite3.connect(DB_PATH)

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

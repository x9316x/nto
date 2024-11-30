from db import connect_db

def insert_initial_data():
    """Добавляет тестовые данные в базу при первом запуске."""
    conn = connect_db()
    cursor = conn.cursor()

    # Проверка существования данных
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] > 0:
        print("Тестовые данные уже существуют.")
        conn.close()
        return

    # Добавляем виды лесопродукции
    products = [
        ("Сырые пиломатериалы",),
        ("Сухие пиломатериалы",),
        ("Строганные доски",),
        ("Рейки",),
        ("Брус",),
        ("Пеллеты",)
    ]
    cursor.executemany("INSERT INTO products (name) VALUES (?)", products)

    # Добавляем клиентов
    clients = [
        ("Иван Иванов", "1234567890", "ivanov@mail.com"),
        ("Петр Петров", "0987654321", "petrov@mail.com"),
        ("Анна Смирнова", "1122334455", "smirnova@mail.com")
    ]
    cursor.executemany("INSERT INTO clients (contact_person, phone, email) VALUES (?, ?, ?)", clients)

    # Добавляем статусы заказа
    statuses = [
        ("Черновик",),
        ("Согласован клиентом",),
        ("Принят в производство",),
        ("Выполнен",)
    ]
    cursor.executemany("INSERT INTO order_status (status_name) VALUES (?)", statuses)

    # Добавляем заказы
    orders = [
        # Заказы с видом лесопродукции: "Сырые пиломатериалы", "Сухие пиломатериалы", "Рейки"
        ("2024-11-01", "2024-11-15", 1, 1, 50, "Требуется доставка до склада", 2),  # Сырые пиломатериалы
        ("2024-11-02", "2024-11-20", 2, 2, 100, "Особые условия хранения", 2),    # Сухие пиломатериалы
        ("2024-11-03", "2024-11-25", 3, 4, 30, "Доставка в течение дня", 2),     # Рейки
    ]
    cursor.executemany("""
        INSERT INTO orders (order_date, due_date, client_id, product_id, quantity, additional_info, status_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, orders)

    # Добавляем цеха завода
    workshops = [
        ("Лесопильный цех",),
        ("Сушильный комплекс",),
        ("Цех строжки и обработки",),
        ("Пеллетный цех",)
    ]
    cursor.executemany("INSERT INTO workshops (name) VALUES (?)", workshops)

    conn.commit()
    conn.close()
    print("Тестовые данные добавлены успешно!")

if __name__ == "__main__":
    insert_initial_data()

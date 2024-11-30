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

    # Получение ID цехов
    cursor.execute("SELECT id FROM workshops WHERE name = 'Лесопильный цех'")
    sawmill_id = cursor.fetchone()[0]
    cursor.execute("SELECT id FROM workshops WHERE name = 'Сушильный комплекс'")
    drying_id = cursor.fetchone()[0]
    cursor.execute("SELECT id FROM workshops WHERE name = 'Цех строжки и обработки'")
    planing_id = cursor.fetchone()[0]
    cursor.execute("SELECT id FROM workshops WHERE name = 'Пеллетный цех'")
    pellet_id = cursor.fetchone()[0]

    # Добавляем участки
    sections = [
        ("Лесопильная линия №1", sawmill_id, "Используется для распиловки тонкомеров, например, реек."),
        ("Лесопильная линия №2", sawmill_id, "Используется для распиловки среднего леса."),
        ("Сушильная камера №1", drying_id, "Камера для интенсивной сушки древесины."),
        ("Сушильная камера №2", drying_id, "Используется для сушки до 15% влажности."),
        ("Сушильная камера №3", drying_id, "Подходит для ускоренной сушки."),
        ("Сушильная камера №4", drying_id, "Стандартная камера для работы с массивом."),
        ("Линия строжки №1", planing_id, "Используется для строжки тонкомеров."),
        ("Линия строжки №2", planing_id, "Используется для строжки среднего леса."),
        ("Линия строжки №3", planing_id, "Используется для строжки среднего леса."),
        ("Дробилка", pellet_id, "Оборудование для измельчения древесных остатков."),
        ("Сушилка", pellet_id, "Оборудование для удаления лишней влаги."),
        ("Гранулятор №1", pellet_id, "Производит гранулы диаметром 6 мм."),
        ("Гранулятор №2", pellet_id, "Производит гранулы диаметром 8 мм."),
    ]
    cursor.executemany("INSERT INTO sections (name, workshop_id, description) VALUES (?, ?, ?)", sections)

    conn.commit()
    conn.close()
    print("Тестовые данные добавлены успешно!")

if __name__ == "__main__":
    insert_initial_data()

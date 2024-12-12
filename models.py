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
        ("Игорь Сидоров", "88005553535", "prosche@mail.com"),
        ("Ирина Семенова", "111222333", "sema@mail.com"),
        ("Алла Денисова", "2468163264", "denisova@mail.com")
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
        ("2024-11-01", "2025-01-15", 1, 1, 50, "Требуется доставка до склада", 2),  # Сырые пиломатериалы
        ("2024-11-02", "2025-01-20", 2, 2, 100, "Особые условия хранения", 2),    # Сухие пиломатериалы
        ("2024-11-03", "2025-01-25", 3, 4, 30, "Доставка в течение дня", 2),     # Рейки
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

    # Добавляем задания на производство
    production_tasks = [
        ("2024-12-01", "2025-01-05", 1, "Сырые пиломатериалы", 50, str(sawmill_id), "Задание для лесопильного цеха."),
        ("2024-12-02", "2025-01-15", 2, "Сухие пиломатериалы", 100, f"{sawmill_id},{drying_id}", "Для лесопильного и сушильного цехов."),
        ("2024-12-03", "2025-01-20", 3, "Рейки", 30, f"{sawmill_id},{drying_id},{planing_id}", "Для всех цехов."),
    ]
    cursor.executemany("""
        INSERT INTO production_tasks (registration_date, start_date, order_id, product_id, quantity, workshops, additional_info)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, production_tasks)

    # Добавляем задания на подготовку
    preparation_tasks = [
        ("2024-12-02", "2025-01-05", 1, 1, "Подготовка лесопильной линии №1", "Создано"),
        ("2024-12-10", "2025-01-14", 2, 2, "Подготовка сушильной камеры №1", "Создано"),
        ("2024-12-15", "2025-01-18", 3, 2, "Подготовка линии строжки №1", "Создано")
    ]
    cursor.executemany("""
        INSERT INTO preparation_tasks (registration_date, required_date, production_task_id, section_id, additional_info, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, preparation_tasks)

    # Обновляем статусы заказов на "Принят в производство"
    cursor.execute("""
        UPDATE orders
        SET status_id = (SELECT id FROM order_status WHERE status_name = 'Принят в производство')
        WHERE id IN (1, 2, 3)
    """)


    # Добавляем задания на смену
    shift_tasks = [
        ("2024-12-12", 1, "2025-01-01", "Лесопильная линия №1", "Не загружать лесопильную линию выше 70-ти %."),
        ("2024-12-12", 2, "2025-01-01", "Дробилка", "После работы провести обслуживание дробилки."),
        ("2024-12-12", 3, "2025-01-02", "Сушильная камера №1", "Сушить на высоких температурах запрещено!"),
    ]
    cursor.executemany("""
        INSERT INTO shift_tasks (creation_date, production_task_id, shift_date, section_name, additional_info)
        VALUES (?, ?, ?, ?, ?)
    """, shift_tasks)

    # Добавляем занятость участков
    section_availability = [
        (1, "2025-01-01"),
        (2, "2025-01-01"),
        (3, "2025-01-02"),
    ]
    cursor.executemany("""
        INSERT INTO section_availability (section_id, date)
        VALUES (?, ?)
    """, section_availability)
    
    conn.commit()
    conn.close()
    print("Тестовые данные успешно добавлены!")

if __name__ == "__main__":
    insert_initial_data()

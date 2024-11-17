from db import connect_db

def insert_initial_data():
    """Добавляет тестовые данные в базу."""
    conn = connect_db()
    cursor = conn.cursor()

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

    # Добавляем статусы заказа
    statuses = [
        ("Черновик",),
        ("Согласован клиентом",),
        ("Принят в производство",),
        ("Выполнен",)
    ]
    cursor.executemany("INSERT INTO order_status (status_name) VALUES (?)", statuses)

    conn.commit()
    conn.close()
    print("Тестовые данные добавлены успешно!")

if __name__ == "__main__":
    insert_initial_data()

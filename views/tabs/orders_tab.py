from tkinter import ttk
from tkinter import simpledialog, messagebox
from db import connect_db

class OrdersTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        parent.add(self.frame, text="Заказы")
        self.setup_tab()

    def setup_tab(self):
        """Настраивает вкладку."""
        ttk.Label(self.frame, text="Список заказов").pack(pady=10)

        # Таблица
        self.tree = ttk.Treeview(self.frame, columns=("ID", "Order Date", "Due Date", "Client", "Product", "Quantity", "Status"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Order Date", text="Дата регистрации")
        self.tree.heading("Due Date", text="Дата выполнения")
        self.tree.heading("Client", text="Клиент")
        self.tree.heading("Product", text="Продукт")
        self.tree.heading("Quantity", text="Количество")
        self.tree.heading("Status", text="Статус")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        # Кнопки управления
        buttons_frame = ttk.Frame(self.frame)
        buttons_frame.pack(pady=10)

        ttk.Button(buttons_frame, text="Создать заказ", command=self.create_order).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Удалить заказ", command=self.delete_order).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Изменить статус", command=self.change_order_status).pack(side="left", padx=5)

        # Загрузка данных
        self.load_orders()

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
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Заполняем таблицу данными
        for row in rows:
            self.tree.insert("", "end", values=row)

    def create_order(self):
        """Создаёт новый заказ."""
        client_id = simpledialog.askinteger("Новый заказ", "Введите ID клиента:")
        product_id = simpledialog.askinteger("Новый заказ", "Введите ID продукта:")
        quantity = simpledialog.askinteger("Новый заказ", "Введите количество продукции:")
        due_date = simpledialog.askstring("Новый заказ", "Введите дату выполнения (ГГГГ-ММ-ДД):")

        if not client_id or not product_id or not quantity or not due_date:
            messagebox.showwarning("Ошибка", "Все поля должны быть заполнены!")
            return

        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO orders (order_date, due_date, client_id, product_id, quantity, status_id)
                VALUES (DATE('now'), ?, ?, ?, ?, 1)
            """, (due_date, client_id, product_id, quantity))
            conn.commit()
            messagebox.showinfo("Успех", "Заказ успешно создан!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось создать заказ: {e}")
        finally:
            conn.close()

        self.load_orders()

    def delete_order(self):
        """Удаляет выбранный заказ."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Ошибка", "Выберите заказ для удаления!")
            return

        order_id = self.tree.item(selected_item, "values")[0]
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM orders WHERE id = ?", (order_id,))
        conn.commit()
        conn.close()

        self.load_orders()
        messagebox.showinfo("Успех", f"Заказ с ID {order_id} удалён!")

    def change_order_status(self):
        """Изменяет статус выбранного заказа."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Ошибка", "Выберите заказ для изменения статуса!")
            return

        order_id, _, _, _, _, _, current_status = self.tree.item(selected_item, "values")
        new_status = simpledialog.askinteger(
            "Изменить статус",
            "Введите ID нового статуса (1: Черновик, 2: Согласован, 3: Принят, 4: Выполнен):"
        )

        if not new_status or new_status < 1 or new_status > 4:
            messagebox.showwarning("Ошибка", "Некорректный статус!")
            return

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE orders SET status_id = ? WHERE id = ?", (new_status, order_id))
        conn.commit()
        conn.close()

        self.load_orders()
        messagebox.showinfo("Успех", f"Статус заказа с ID {order_id} изменён на {new_status}!")

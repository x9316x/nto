from tkinter import ttk, Toplevel, messagebox
from tkinter import StringVar, IntVar
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
        self.tree = ttk.Treeview(
            self.frame,
            columns=("ID", "Order Date", "Due Date", "Client", "Product", "Quantity", "Status"),
            show="headings"
        )
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
        """Создаёт новый заказ с выпадающими списками."""
        form = Toplevel(self.frame)
        form.title("Создать заказ")
        form.geometry("400x300")

        client_var = StringVar()
        product_var = StringVar()
        quantity_var = IntVar()
        due_date_var = StringVar()
        status_var = StringVar()

        # Получение данных из базы для выпадающих списков
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, contact_person FROM clients")
        clients = cursor.fetchall()
        cursor.execute("SELECT id, name FROM products")
        products = cursor.fetchall()
        cursor.execute("SELECT id, status_name FROM order_status")
        statuses = cursor.fetchall()
        conn.close()

        ttk.Label(form, text="Клиент:").pack(pady=5)
        client_combobox = ttk.Combobox(form, textvariable=client_var, values=[f"{c[0]}: {c[1]}" for c in clients])
        client_combobox.pack(fill="x", padx=10)

        ttk.Label(form, text="Продукт:").pack(pady=5)
        product_combobox = ttk.Combobox(form, textvariable=product_var, values=[f"{p[0]}: {p[1]}" for p in products])
        product_combobox.pack(fill="x", padx=10)

        ttk.Label(form, text="Количество:").pack(pady=5)
        ttk.Entry(form, textvariable=quantity_var).pack(fill="x", padx=10)

        ttk.Label(form, text="Дата выполнения (ГГГГ-ММ-ДД):").pack(pady=5)
        ttk.Entry(form, textvariable=due_date_var).pack(fill="x", padx=10)

        ttk.Label(form, text="Статус:").pack(pady=5)
        status_combobox = ttk.Combobox(form, textvariable=status_var, values=[f"{s[0]}: {s[1]}" for s in statuses])
        status_combobox.pack(fill="x", padx=10)

        def save_order():
            try:
                client_id = int(client_var.get().split(":")[0])
                product_id = int(product_var.get().split(":")[0])
                status_id = int(status_var.get().split(":")[0])
                quantity = quantity_var.get()
                due_date = due_date_var.get()

                if not client_id or not product_id or not quantity or not due_date or not status_id:
                    messagebox.showwarning("Ошибка", "Все поля должны быть заполнены!")
                    return

                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO orders (order_date, due_date, client_id, product_id, quantity, status_id)
                    VALUES (DATE('now'), ?, ?, ?, ?, ?)
                """, (due_date, client_id, product_id, quantity, status_id))
                conn.commit()
                conn.close()
                messagebox.showinfo("Успех", "Заказ успешно создан!")
                self.load_orders()
                form.destroy()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось создать заказ: {e}")

        ttk.Button(form, text="Сохранить", command=save_order).pack(pady=10)

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
        status_var = StringVar()

        # Получение статусов из базы
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, status_name FROM order_status")
        statuses = cursor.fetchall()
        conn.close()

        form = Toplevel(self.frame)
        form.title("Изменить статус")
        form.geometry("300x150")

        ttk.Label(form, text="Статус:").pack(pady=5)
        status_combobox = ttk.Combobox(form, textvariable=status_var, values=[f"{s[0]}: {s[1]}" for s in statuses])
        status_combobox.pack(fill="x", padx=10)

        def update_status():
            try:
                status_id = int(status_var.get().split(":")[0])
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("UPDATE orders SET status_id = ? WHERE id = ?", (status_id, order_id))
                conn.commit()
                conn.close()
                self.load_orders()
                form.destroy()
                messagebox.showinfo("Успех", f"Статус заказа с ID {order_id} изменён!")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось изменить статус: {e}")

        ttk.Button(form, text="Сохранить", command=update_status).pack(pady=10)

from tkinter import ttk, Toplevel, messagebox, Text
from tkinter import StringVar, IntVar
from db import connect_db
import datetime  # Для работы с датами

class OrdersTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        parent.add(self.frame, text="Заказы")
        self.setup_tab()

    def setup_tab(self):
        """Настраивает вкладку."""
        # Заголовок
        ttk.Label(self.frame, text="Список заказов").pack(pady=10)

        # Таблица
        self.tree = ttk.Treeview(
            self.frame,
            columns=("ID", "Order Date", "Due Date", "Client", "Product", "Quantity", "Status", "Additional Info"),
            show="headings"
        )
        self.tree.heading("ID", text="ID")
        self.tree.heading("Order Date", text="Дата регистрации")
        self.tree.heading("Due Date", text="Дата выполнения")
        self.tree.heading("Client", text="Клиент")
        self.tree.heading("Product", text="Продукт")
        self.tree.heading("Quantity", text="Количество")
        self.tree.heading("Status", text="Статус")
        self.tree.heading("Additional Info", text="Дополнительная информация")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)  # Таблица заполняет всё доступное пространство

        # Кнопки управления
        buttons_frame = ttk.Frame(self.frame)
        buttons_frame.pack(pady=10)

        ttk.Button(buttons_frame, text="Создать заказ", command=self.create_order).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Удалить заказ", command=self.delete_order).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Редактировать заказ", command=self.edit_order).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Согласовать заказ", command=self.approve_order).pack(side="left", padx=5)

        # Загрузка данных
        self.load_orders()

        # Центрируем окно после настройки содержимого
        self.frame.update_idletasks()  # Обновляем геометрию окна
        parent_window = self.frame.winfo_toplevel()
        parent_window.geometry("")  # Устанавливаем автоматический размер

    def load_orders(self):
        """Загружает данные о заказах из базы с цветовым выделением по статусу."""
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT o.id, 
                o.order_date, 
                COALESCE(o.due_date, 'Дата не указана') AS due_date, 
                COALESCE(c.contact_person, '') AS client, 
                COALESCE(p.name, '') AS product, 
                COALESCE(o.quantity, 0) AS quantity, 
                COALESCE(s.status_name, 'Черновик') AS status,
                COALESCE(o.additional_info, 'Нет дополнительной информации') AS additional_info
            FROM orders o
            LEFT JOIN clients c ON o.client_id = c.id
            LEFT JOIN products p ON o.product_id = p.id
            LEFT JOIN order_status s ON o.status_id = s.id
        """)
        rows = cursor.fetchall()
        conn.close()

        # Очищаем таблицу перед загрузкой
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Настройка цветовых тегов
        self.tree.tag_configure("draft", background="white")  # Черновик
        self.tree.tag_configure("client_approved", background="orange")  # Согласован клиентом
        self.tree.tag_configure("in_production", background="yellow")  # Принят в производство
        self.tree.tag_configure("completed", background="green")  # Выполнен

        # Заполняем таблицу данными
        for row in rows:
            status = row[6]
            if status == "Черновик":
                tag = "draft"
            elif status == "Согласован клиентом":
                tag = "client_approved"
            elif status == "Принят в производство":
                tag = "in_production"
            elif status == "Выполнен":
                tag = "completed"
            else:
                tag = ""  # Для любых других статусов

            self.tree.insert("", "end", values=row, tags=(tag,))

    def create_order(self):
        """Создаёт новый заказ с пустой формой."""
        self.order_form()

    def edit_order(self):
        """Редактирует существующий заказ."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Ошибка", "Выберите заказ для редактирования!")
            return

        # Получение данных заказа
        order_data = self.tree.item(selected_item, "values")
        order_id = order_data[0]
        order_date = order_data[1]
        due_date = order_data[2]
        client = order_data[3]
        product = order_data[4]
        quantity = order_data[5]
        status = order_data[6]
        additional_info = order_data[7]

        # Открытие формы редактирования
        self.order_form(order_id, order_date, due_date, client, product, quantity, status, additional_info)

    def order_form(self, order_id=None, order_date=None, due_date=None, client=None, product=None, quantity=None, status=None, additional_info=None):
        """Форма для создания или редактирования заказа."""
        form = Toplevel(self.frame)
        form.title("Редактировать заказ" if order_id else "Создать заказ")
        form.geometry("400x500")

        client_var = StringVar(value=client)
        product_var = StringVar(value=product)
        quantity_var = IntVar(value=int(quantity) if quantity else 0)
        due_date_var = StringVar(value=due_date)

        # Получение данных из базы для выпадающих списков
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, contact_person FROM clients")
        clients = cursor.fetchall()
        cursor.execute("SELECT id, name FROM products")
        products = cursor.fetchall()
        conn.close()

        ttk.Label(form, text="Клиент:").pack(pady=5)
        client_combobox = ttk.Combobox(form, textvariable=client_var, values=[c[1] for c in clients])
        client_combobox.pack(fill="x", padx=10)

        ttk.Label(form, text="Продукт:").pack(pady=5)
        product_combobox = ttk.Combobox(form, textvariable=product_var, values=[p[1] for p in products])
        product_combobox.pack(fill="x", padx=10)

        ttk.Label(form, text="Количество:").pack(pady=5)
        ttk.Entry(form, textvariable=quantity_var).pack(fill="x", padx=10)

        ttk.Label(form, text="Дата выполнения (ГГГГ-ММ-ДД):").pack(pady=5)
        ttk.Entry(form, textvariable=due_date_var).pack(fill="x", padx=10)

        ttk.Label(form, text="Дополнительная информация:").pack(pady=5)
        additional_info_text = Text(form, height=5, wrap="word")
        additional_info_text.pack(fill="both", padx=10, pady=5)
        if additional_info:  # Если есть существующее значение, вставляем его в текстовое поле
            additional_info_text.insert("1.0", additional_info)

        def save_order():
            try:
                # Извлечение данных из текстового поля
                additional_info = additional_info_text.get("1.0", "end").strip()

                # Проверка полей
                client_id = next((c[0] for c in clients if c[1] == client_var.get()), None)
                product_id = next((p[0] for p in products if p[1] == product_var.get()), None)
                quantity = quantity_var.get()
                due_date = due_date_var.get()

                # Сохранение данных
                with connect_db() as conn:
                    cursor = conn.cursor()
                    if order_id:
                        cursor.execute("""
                            UPDATE orders SET due_date = ?, client_id = ?, product_id = ?, quantity = ?, additional_info = ?
                            WHERE id = ?
                        """, (due_date, client_id, product_id, quantity, additional_info, order_id))
                    else:
                        cursor.execute("""
                            INSERT INTO orders (order_date, due_date, client_id, product_id, quantity, status_id, additional_info)
                            VALUES (DATE('now'), ?, ?, ?, ?, 1, ?)
                        """, (due_date, client_id, product_id, quantity, additional_info))
                    conn.commit()

                self.load_orders()
                form.destroy()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка сохранения: {e}")

        ttk.Button(form, text="Сохранить", command=save_order).pack(pady=10)

    def approve_order(self):
        """Согласовывает выбранный заказ."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Ошибка", "Выберите заказ для согласования!")
            return

        order_id = self.tree.item(selected_item, "values")[0]
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT client_id, product_id, quantity FROM orders WHERE id = ?", (order_id,))
            order = cursor.fetchone()

            if not order or not order[0] or not order[1] or order[2] <= 0:
                messagebox.showwarning("Ошибка", "Для согласования заполните поля клиент, продукт и количество > 0!")
                return

            cursor.execute("UPDATE orders SET status_id = 2 WHERE id = ?", (order_id,))
            conn.commit()

        self.load_orders()
        messagebox.showinfo("Успех", f"Заказ ID {order_id} согласован!")

    def delete_order(self):
        """Удаляет выбранный заказ."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Ошибка", "Выберите заказ для удаления!")
            return

        order_id = self.tree.item(selected_item, "values")[0]
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM orders WHERE id = ?", (order_id,))
            conn.commit()

        self.load_orders()
        messagebox.showinfo("Успех", f"Заказ ID {order_id} удалён!")

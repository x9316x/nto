from tkinter import ttk, messagebox, Toplevel, Label, Entry, Text, Button, IntVar
from db import connect_db
import datetime

class ProductionTasksTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        parent.add(self.frame, text="Задания на производство")
        self.setup_tab()

    def setup_tab(self):
        """Настраивает вкладку."""
        ttk.Label(self.frame, text="Список заказов со статусами 'Согласован клиентом' и 'Принят в производство'").pack(pady=10)

        # Таблица для отображения заказов
        self.tree = ttk.Treeview(self.frame, columns=("ID", "Order Date", "Due Date", "Client", "Product", "Quantity", "Status"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Order Date", text="Дата заказа")
        self.tree.heading("Due Date", text="Срок выполнения")
        self.tree.heading("Client", text="Клиент")
        self.tree.heading("Product", text="Продукция")
        self.tree.heading("Quantity", text="Количество")
        self.tree.heading("Status", text="Статус")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        # Кнопка "Зарегистрировать задание на производство"
        Button(self.frame, text="Зарегистрировать задание", command=self.open_task_registration_form).pack(pady=10)

        # Загрузка данных
        self.load_orders()

    def load_orders(self):
        """Загружает заказы со статусами 'Согласован клиентом' и 'Принят в производство'."""
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT orders.id, orders.order_date, orders.due_date, clients.contact_person, products.name, orders.quantity, order_status.status_name
            FROM orders
            JOIN clients ON orders.client_id = clients.id
            JOIN products ON orders.product_id = products.id
            JOIN order_status ON orders.status_id = order_status.id
            WHERE order_status.status_name IN ('Согласован клиентом', 'Принят в производство')
        """)
        rows = cursor.fetchall()
        conn.close()

        # Очищаем таблицу перед загрузкой
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Заполняем таблицу данными
        for row in rows:
            self.tree.insert("", "end", values=row)

    def open_task_registration_form(self):
        """Открывает форму для регистрации задания на производство."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Ошибка", "Выберите заказ для регистрации задания!")
            return

        order_id, order_date, due_date, client, product, quantity, status = self.tree.item(selected_item, "values")

        form = Toplevel(self.frame)
        form.title("Регистрация задания на производство")
        form.geometry("400x500")

        # Поля формы
        Label(form, text="Дата регистрации задания").pack(pady=5)
        registration_date_label = Label(form, text=datetime.date.today().strftime("%Y-%m-%d"))
        registration_date_label.pack(pady=5)

        Label(form, text="Дата начала выполнения задания").pack(pady=5)
        start_date_entry = Entry(form)
        start_date_entry.pack(pady=5, fill="x", padx=10)

        Label(form, text="ID заказа").pack(pady=5)
        Label(form, text=order_id).pack(pady=5)

        Label(form, text="Продукция").pack(pady=5)
        Label(form, text=product).pack(pady=5)

        Label(form, text="Количество").pack(pady=5)
        Label(form, text=quantity).pack(pady=5)

        Label(form, text="Выберите цеха").pack(pady=5)
        workshops_frame = ttk.Frame(form)
        workshops_frame.pack(pady=5, fill="both", padx=10)
        self.create_workshop_checkboxes(workshops_frame, product)

        Label(form, text="Дополнительная информация").pack(pady=5)
        additional_info_text = Text(form, height=5)
        additional_info_text.pack(pady=5, fill="both", padx=10)

        def save_task():
            """Сохраняет задание на производство в базу данных."""
            start_date = start_date_entry.get().strip()
            workshops = ",".join([str(id) for id, var in self.workshop_checkboxes.items() if var.get()])
            additional_info = additional_info_text.get("1.0", "end").strip()

            if not start_date:
                messagebox.showwarning("Ошибка", "Дата начала выполнения задания обязательна!")
                return

            try:
                start_date_obj = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
                registration_date_obj = datetime.date.today()
                if start_date_obj < registration_date_obj:
                    messagebox.showwarning("Ошибка", "Дата начала выполнения не может быть раньше даты регистрации!")
                    return
            except ValueError:
                messagebox.showwarning("Ошибка", "Введите дату начала выполнения задания в формате YYYY-MM-DD!")
                return

            if not workshops:
                messagebox.showwarning("Ошибка", "Выберите хотя бы один цех для выполнения задания!")
                return

            conn = connect_db()
            cursor = conn.cursor()
            
            # Сохранение задания на производство
            cursor.execute("""
                INSERT INTO production_tasks (registration_date, start_date, order_id, product_id, quantity, workshops, additional_info)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (registration_date_label.cget("text"), start_date, order_id, product, quantity, workshops, additional_info))

            # Обновление статуса заказа
            cursor.execute("""
                UPDATE orders
                SET status_id = (SELECT id FROM order_status WHERE status_name = 'Принят в производство')
                WHERE id = ?
            """, (order_id,))
            
            conn.commit()
            conn.close()

            self.load_orders()  # Обновляем список заказов с новым статусом
            form.destroy()
            messagebox.showinfo("Успех", f"Задание на производство зарегистрировано и статус заказа обновлён!")

        Button(form, text="Сохранить", command=save_task).pack(pady=10)

    def create_workshop_checkboxes(self, parent, product_name):
        """Создаёт чекбоксы для выбора цехов на основе типа продукции."""
        self.workshop_checkboxes = {}

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM workshops")
        workshops = cursor.fetchall()
        conn.close()

        # Логика выбора цехов на основе продукции
        allowed_workshops = []
        if product_name == "Сырые пиломатериалы":
            allowed_workshops = ["Лесопильный цех"]
        elif product_name == "Сухие пиломатериалы":
            allowed_workshops = ["Лесопильный цех", "Сушильный комплекс"]
        elif product_name in ["Строганные доски", "Рейки", "Брус"]:
            allowed_workshops = ["Лесопильный цех", "Сушильный комплекс", "Цех строжки и обработки"]
        elif product_name == "Пеллеты":
            allowed_workshops = ["Пеллетный цех"]

        for workshop_id, workshop_name in workshops:
            if workshop_name in allowed_workshops:
                var = IntVar(value=0)  # Используем IntVar из tkinter
                checkbox = ttk.Checkbutton(parent, text=workshop_name, variable=var)
                checkbox.pack(anchor="w")
                self.workshop_checkboxes[workshop_id] = var

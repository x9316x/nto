from tkinter import ttk, Toplevel, messagebox
from tkinter import StringVar
from db import connect_db

class ClientsTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        parent.add(self.frame, text="Клиенты")
        self.setup_tab()

    def setup_tab(self):
        """Настраивает вкладку."""
        ttk.Label(self.frame, text="Список клиентов").pack(pady=10)

        # Таблица
        self.tree = ttk.Treeview(self.frame, columns=("ID", "Contact", "Phone", "Email"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Contact", text="Контактное лицо")
        self.tree.heading("Phone", text="Телефон")
        self.tree.heading("Email", text="Email")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        # Кнопки управления
        buttons_frame = ttk.Frame(self.frame)
        buttons_frame.pack(pady=10)

        ttk.Button(buttons_frame, text="Добавить", command=self.open_add_client_form).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Удалить", command=self.delete_client).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Редактировать", command=self.open_edit_client_form).pack(side="left", padx=5)

        # Загрузка данных
        self.load_clients()

    def load_clients(self):
        """Загружает данные из базы."""
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, contact_person, phone, email FROM clients")
        rows = cursor.fetchall()
        conn.close()

        # Очищаем таблицу перед загрузкой
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Заполняем таблицу данными
        for row in rows:
            self.tree.insert("", "end", values=row)

    def open_add_client_form(self):
        """Открывает форму для добавления клиента."""
        self.open_client_form("Добавить клиента")

    def open_edit_client_form(self):
        """Открывает форму для редактирования клиента."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Ошибка", "Выберите клиента для редактирования!")
            return

        client_data = self.tree.item(selected_item, "values")
        self.open_client_form("Редактировать клиента", client_data)

    def open_client_form(self, title, client_data=None):
        """Открывает форму для добавления или редактирования клиента."""
        form = Toplevel(self.frame)
        form.title(title)
        form.geometry("300x200")

        contact_var = StringVar(value=client_data[1] if client_data else "")
        phone_var = StringVar(value=client_data[2] if client_data else "")
        email_var = StringVar(value=client_data[3] if client_data else "")

        ttk.Label(form, text="Контактное лицо:").pack(pady=5)
        contact_entry = ttk.Entry(form, textvariable=contact_var)
        contact_entry.pack(fill="x", padx=10)

        ttk.Label(form, text="Телефон:").pack(pady=5)
        phone_entry = ttk.Entry(form, textvariable=phone_var)
        phone_entry.pack(fill="x", padx=10)

        ttk.Label(form, text="Email:").pack(pady=5)
        email_entry = ttk.Entry(form, textvariable=email_var)
        email_entry.pack(fill="x", padx=10)

        # Кнопка для сохранения
        def save_client():
            contact = contact_var.get()
            phone = phone_var.get()
            email = email_var.get()

            if not contact or not phone or not email:
                # Сообщение об ошибке, но окно остаётся открытым
                messagebox.showwarning("Ошибка", "Все поля должны быть заполнены!")
                return

            conn = connect_db()
            cursor = conn.cursor()

            if client_data:  # Если данные клиента уже существуют, это редактирование
                client_id = client_data[0]
                cursor.execute(
                    "UPDATE clients SET contact_person = ?, phone = ?, email = ? WHERE id = ?",
                    (contact, phone, email, client_id),
                )
                messagebox.showinfo("Успех", f"Клиент с ID {client_id} обновлён!")
            else:  # Если данных нет, это добавление
                cursor.execute(
                    "INSERT INTO clients (contact_person, phone, email) VALUES (?, ?, ?)",
                    (contact, phone, email),
                )
                messagebox.showinfo("Успех", f"Клиент '{contact}' добавлен!")

            conn.commit()
            conn.close()
            self.load_clients()
            form.destroy()  # Закрываем окно только при успешном сохранении

        ttk.Button(form, text="Сохранить", command=save_client).pack(pady=10)

    def delete_client(self):
        """Удаляет выбранного клиента."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Ошибка", "Выберите клиента для удаления!")
            return

        client_id = self.tree.item(selected_item, "values")[0]
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clients WHERE id = ?", (client_id,))
        conn.commit()
        conn.close()

        self.load_clients()
        messagebox.showinfo("Успех", f"Клиент с ID {client_id} удалён!")

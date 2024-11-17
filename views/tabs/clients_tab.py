from tkinter import ttk
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

        ttk.Button(buttons_frame, text="Добавить", command=self.add_client).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Удалить", command=self.delete_client).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Редактировать", command=self.edit_client).pack(side="left", padx=5)

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

    def add_client(self):
        """Добавляет клиента."""
        # Пример: Открыть окно для ввода данных клиента
        print("Добавление клиента")

    def delete_client(self):
        """Удаляет выбранного клиента."""
        selected_item = self.tree.selection()
        if not selected_item:
            print("Клиент не выбран")
            return

        client_id = self.tree.item(selected_item, "values")[0]
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clients WHERE id = ?", (client_id,))
        conn.commit()
        conn.close()

        self.load_clients()
        print(f"Клиент с ID {client_id} удалён.")

    def edit_client(self):
        """Редактирует выбранного клиента."""
        selected_item = self.tree.selection()
        if not selected_item:
            print("Клиент не выбран")
            return

        client_id = self.tree.item(selected_item, "values")[0]
        print(f"Редактирование клиента с ID {client_id}")
        # Открыть окно для редактирования данных клиента

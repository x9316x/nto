from tkinter import ttk, simpledialog, messagebox
from db import connect_db

class WorkshopsTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        parent.add(self.frame, text="Цеха завода")
        self.setup_tab()

    def setup_tab(self):
        """Настраивает вкладку."""
        ttk.Label(self.frame, text="Список цехов завода").pack(pady=10)

        # Таблица для отображения цехов
        self.tree = ttk.Treeview(self.frame, columns=("ID", "Name"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Название")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        # Кнопки управления
        buttons_frame = ttk.Frame(self.frame)
        buttons_frame.pack(pady=10)

        ttk.Button(buttons_frame, text="Добавить", command=self.add_workshop).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Удалить", command=self.delete_workshop).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Редактировать", command=self.edit_workshop).pack(side="left", padx=5)

        # Загрузка данных
        self.load_workshops()

    def load_workshops(self):
        """Загружает данные о цехах завода из базы."""
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM workshops")
        rows = cursor.fetchall()
        conn.close()

        # Очищаем таблицу перед загрузкой
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Заполняем таблицу данными
        for row in rows:
            self.tree.insert("", "end", values=row)

    def add_workshop(self):
        """Добавляет новый цех завода."""
        workshop_name = simpledialog.askstring("Добавить цех", "Введите название цеха:")
        if not workshop_name:
            return

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO workshops (name) VALUES (?)", (workshop_name,))
        conn.commit()
        conn.close()

        self.load_workshops()
        messagebox.showinfo("Успех", f"Цех '{workshop_name}' добавлен!")

    def delete_workshop(self):
        """Удаляет выбранный цех завода."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Ошибка", "Выберите цех для удаления!")
            return

        workshop_id = self.tree.item(selected_item, "values")[0]
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM workshops WHERE id = ?", (workshop_id,))
        conn.commit()
        conn.close()

        self.load_workshops()
        messagebox.showinfo("Успех", f"Цех с ID {workshop_id} удалён!")

    def edit_workshop(self):
        """Редактирует выбранный цех завода."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Ошибка", "Выберите цех для редактирования!")
            return

        workshop_id, workshop_name = self.tree.item(selected_item, "values")
        new_name = simpledialog.askstring("Редактировать цех", "Введите новое название цеха:", initialvalue=workshop_name)

        if not new_name:
            return

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE workshops SET name = ? WHERE id = ?", (new_name, workshop_id))
        conn.commit()
        conn.close()

        self.load_workshops()
        messagebox.showinfo("Успех", f"Цех с ID {workshop_id} обновлён на '{new_name}'!")

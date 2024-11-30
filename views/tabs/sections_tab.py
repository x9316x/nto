from tkinter import ttk, messagebox, Toplevel, Label, Entry, Text, Button
from db import connect_db

class SectionsTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        parent.add(self.frame, text="Участки")
        self.setup_tab()

    def setup_tab(self):
        """Настраивает вкладку."""
        ttk.Label(self.frame, text="Список участков завода").pack(pady=10)

        # Таблица для отображения участков
        self.tree = ttk.Treeview(self.frame, columns=("ID", "Name", "Workshop", "Description"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Название")
        self.tree.heading("Workshop", text="Цех")
        self.tree.heading("Description", text="Описание")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        # Кнопки управления
        buttons_frame = ttk.Frame(self.frame)
        buttons_frame.pack(pady=10)

        ttk.Button(buttons_frame, text="Добавить", command=self.open_add_section_form).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Удалить", command=self.delete_section).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Редактировать", command=self.open_edit_section_form).pack(side="left", padx=5)

        # Загрузка данных
        self.load_sections()

    def load_sections(self):
        """Загружает данные о участках из базы."""
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT sections.id, sections.name, workshops.name AS workshop, sections.description
            FROM sections
            JOIN workshops ON sections.workshop_id = workshops.id
        """)
        rows = cursor.fetchall()
        conn.close()

        # Очищаем таблицу перед загрузкой
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Заполняем таблицу данными
        for row in rows:
            self.tree.insert("", "end", values=row)

    def open_add_section_form(self):
        """Открывает форму для добавления нового участка."""
        self._open_section_form("Добавить участок", save_action=self.add_section)

    def open_edit_section_form(self):
        """Открывает форму для редактирования выбранного участка."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Ошибка", "Выберите участок для редактирования!")
            return

        section_id, section_name, workshop_name, description = self.tree.item(selected_item, "values")
        self._open_section_form("Редактировать участок", section_id, section_name, workshop_name, description, save_action=self.edit_section)

    def _open_section_form(self, title, section_id=None, section_name="", workshop_name="", description="", save_action=None):
        """Создаёт окно формы для добавления или редактирования участка."""
        form = Toplevel(self.frame)
        form.title(title)
        form.geometry("400x300")

        # Поле для названия участка
        Label(form, text="Название участка").pack(pady=5)
        name_entry = Entry(form)
        name_entry.pack(pady=5, fill="x", padx=10)
        name_entry.insert(0, section_name)

        # Список цехов
        Label(form, text="Выберите цех").pack(pady=5)
        workshop_combobox = ttk.Combobox(form, state="readonly")
        workshop_combobox.pack(pady=5, fill="x", padx=10)

        # Загрузка цехов
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM workshops")
        workshops = cursor.fetchall()
        conn.close()
        workshop_dict = {name: id for id, name in workshops}
        workshop_combobox["values"] = list(workshop_dict.keys())
        if workshop_name:  # Для редактирования выбираем текущий цех
            workshop_combobox.set(workshop_name)

        # Поле для описания участка
        Label(form, text="Описание участка").pack(pady=5)
        description_text = Text(form, height=5)
        description_text.pack(pady=5, fill="both", padx=10)
        description_text.insert("1.0", description)

        # Сохранение изменений
        def save_changes():
            name = name_entry.get().strip()
            selected_workshop = workshop_combobox.get()
            workshop_id = workshop_dict.get(selected_workshop, None)
            desc = description_text.get("1.0", "end").strip()
            if not name or not selected_workshop:
                messagebox.showwarning("Ошибка", "Заполните все обязательные поля!")
                return
            if save_action:
                save_action(section_id, name, workshop_id, desc)
            form.destroy()

        Button(form, text="Сохранить", command=save_changes).pack(pady=10)

    def add_section(self, section_id, name, workshop_id, description):
        """Добавляет новый участок в базу данных."""
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO sections (name, workshop_id, description) VALUES (?, ?, ?)", 
                       (name, workshop_id, description))
        conn.commit()
        conn.close()

        self.load_sections()
        messagebox.showinfo("Успех", f"Участок '{name}' добавлен!")

    def edit_section(self, section_id, name, workshop_id, description):
        """Обновляет информацию об участке в базе данных."""
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE sections SET name = ?, workshop_id = ?, description = ? WHERE id = ?", 
                       (name, workshop_id, description, section_id))
        conn.commit()
        conn.close()

        self.load_sections()
        messagebox.showinfo("Успех", f"Участок с ID {section_id} обновлён!")

    def delete_section(self):
        """Удаляет выбранный участок."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Ошибка", "Выберите участок для удаления!")
            return

        section_id = self.tree.item(selected_item, "values")[0]
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sections WHERE id = ?", (section_id,))
        conn.commit()
        conn.close()

        self.load_sections()
        messagebox.showinfo("Успех", f"Участок с ID {section_id} удалён!")

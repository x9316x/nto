from tkinter import ttk, messagebox, Toplevel, Text, Label, Entry, Button, StringVar
from db import connect_db
import datetime

class PreparationTasksTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        parent.add(self.frame, text="Задания на подготовку/оснастку")
        self.setup_tab()

    def setup_tab(self):
        """Настраивает вкладку."""
        # Заголовок для таблицы заданий на производство
        ttk.Label(self.frame, text="Задания на производство").pack(pady=5)

        # Таблица для отображения заданий на производство
        self.production_tasks_tree = ttk.Treeview(
            self.frame, 
            columns=("ID", "Start Date", "Order ID", "Workshops"), 
            show="headings"
        )
        self.production_tasks_tree.heading("ID", text="ID")
        self.production_tasks_tree.heading("Start Date", text="Дата начала")
        self.production_tasks_tree.heading("Order ID", text="ID Заказа")
        self.production_tasks_tree.heading("Workshops", text="Цеха")
        self.production_tasks_tree.pack(expand=True, fill="both", padx=10, pady=5)

        # Кнопка для регистрации задания на подготовку
        Button(self.frame, text="Зарегистрировать задание на подготовку", command=self.open_task_registration_form).pack(pady=10)

        # Заголовок для таблицы заданий на подготовку
        ttk.Label(self.frame, text="Задания на подготовку/оснастку").pack(pady=5)

        # Таблица для отображения заданий на подготовку
        self.preparation_tasks_tree = ttk.Treeview(
            self.frame, 
            columns=("ID", "Registration Date", "Required Date", "Section", "Status"), 
            show="headings"
        )
        self.preparation_tasks_tree.heading("ID", text="ID")
        self.preparation_tasks_tree.heading("Registration Date", text="Дата регистрации")
        self.preparation_tasks_tree.heading("Required Date", text="Дата выполнения")
        self.preparation_tasks_tree.heading("Section", text="Участок")
        self.preparation_tasks_tree.heading("Status", text="Статус")
        self.preparation_tasks_tree.pack(expand=True, fill="both", padx=10, pady=5)

        # Загрузка данных
        self.load_production_tasks()
        self.load_preparation_tasks()
        
        # Центрируем окно после настройки содержимого
        self.frame.update_idletasks()  # Обновляем геометрию окна
        parent_window = self.frame.winfo_toplevel()
        parent_window.geometry("")  # Устанавливаем автоматический размер

    def load_production_tasks(self):
        """Загружает задания на производство."""
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, start_date, order_id, workshops
            FROM production_tasks
        """)
        rows = cursor.fetchall()
        conn.close()

        # Очищаем таблицу перед загрузкой
        for item in self.production_tasks_tree.get_children():
            self.production_tasks_tree.delete(item)

        # Заполняем таблицу данными
        for row in rows:
            self.production_tasks_tree.insert("", "end", values=row)

    def load_preparation_tasks(self):
        """Загружает задания на подготовку/оснастку."""
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT pt.id, pt.registration_date, pt.required_date, s.name, pt.status
            FROM preparation_tasks pt
            JOIN sections s ON pt.section_id = s.id
        """)
        rows = cursor.fetchall()
        conn.close()

        # Очищаем таблицу перед загрузкой
        for item in self.preparation_tasks_tree.get_children():
            self.preparation_tasks_tree.delete(item)

        # Заполняем таблицу данными
        for row in rows:
            self.preparation_tasks_tree.insert("", "end", values=row)

    def open_task_registration_form(self):
        """Открывает форму для регистрации задания на подготовку/оснастку."""
        selected_item = self.production_tasks_tree.selection()
        if not selected_item:
            messagebox.showwarning("Ошибка", "Выберите задание на производство для регистрации!")
            return

        production_task_id, start_date, order_id, workshops = self.production_tasks_tree.item(selected_item, "values")

        form = Toplevel(self.frame)
        form.title("Регистрация задания на подготовку/оснастку")
        form.geometry("400x600")

        # Поля формы
        Label(form, text="Дата регистрации").pack(pady=5)
        registration_date_label = Label(form, text=datetime.date.today().strftime("%Y-%m-%d"))
        registration_date_label.pack(pady=5)

        Label(form, text="Дата выполнения").pack(pady=5)
        required_date_entry = Entry(form)
        required_date_entry.pack(pady=5, fill="x", padx=10)

        Label(form, text="ID Задания на производство").pack(pady=5)
        Label(form, text=production_task_id).pack(pady=5)

        Label(form, text="Выберите участок").pack(pady=5)
        section_var = StringVar()
        section_combobox = ttk.Combobox(form, textvariable=section_var)
        section_combobox.pack(pady=5, fill="x", padx=10)
        self.load_sections_for_workshops(section_combobox, workshops)

        Label(form, text="Дополнительная информация").pack(pady=5)
        additional_info_text = Text(form, height=5)
        additional_info_text.pack(pady=5, fill="both", padx=10)

        def save_task():
            """Сохраняет задание на подготовку в базу данных."""
            required_date = required_date_entry.get().strip()
            section_name = section_var.get()
            additional_info = additional_info_text.get("1.0", "end").strip()

            if not required_date or not section_name:
                messagebox.showwarning("Ошибка", "Все поля, кроме информации, обязательны для заполнения!")
                return

            try:
                required_date_obj = datetime.datetime.strptime(required_date, "%Y-%m-%d").date()
                if required_date_obj > datetime.datetime.strptime(start_date, "%Y-%m-%d").date():
                    messagebox.showwarning("Ошибка", "Дата выполнения должна быть раньше даты начала производства!")
                    return
            except ValueError:
                messagebox.showwarning("Ошибка", "Введите дату выполнения в формате YYYY-MM-DD!")
                return

            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM sections WHERE name = ?", (section_name,))
            section_id = cursor.fetchone()
            if not section_id:
                messagebox.showerror("Ошибка", "Указанный участок не найден!")
                return

            cursor.execute("""
                INSERT INTO preparation_tasks (registration_date, required_date, production_task_id, section_id, additional_info)
                VALUES (?, ?, ?, ?, ?)
            """, (registration_date_label.cget("text"), required_date, production_task_id, section_id[0], additional_info))
            conn.commit()
            conn.close()

            self.load_preparation_tasks()
            form.destroy()
            messagebox.showinfo("Успех", "Задание на подготовку зарегистрировано!")

        Button(form, text="Сохранить", command=save_task).pack(pady=10)

    def load_sections_for_workshops(self, combobox, workshops):
        """Загружает участки, соответствующие выбранным цехам."""
        workshop_ids = [int(w.strip()) for w in workshops.split(",")]
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.name 
            FROM sections s
            WHERE s.workshop_id IN ({})
        """.format(",".join("?" * len(workshop_ids))), workshop_ids)
        sections = cursor.fetchall()
        conn.close()
        combobox["values"] = [s[0] for s in sections]

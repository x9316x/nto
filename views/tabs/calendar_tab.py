from tkinter import ttk, Label, Entry, Button, Toplevel, Text, messagebox
from db import connect_db
import datetime


class CalendarTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        parent.add(self.frame, text="Календарь рабочих смен")
        self.setup_tab()

    def setup_tab(self):
        """Настраивает вкладку."""
        # Заголовок
        Label(self.frame, text="Календарь рабочих смен").pack(pady=10)

        # Поле для выбора даты
        Label(self.frame, text="Выберите дату (YYYY-MM-DD):").pack(pady=5)
        self.date_entry = Entry(self.frame)
        self.date_entry.pack(pady=5, padx=10, fill="x")

        # Кнопка для загрузки данных
        Button(self.frame, text="Показать свободные участки", command=self.load_free_sections).pack(pady=10)

        # Таблица для отображения свободных участков
        self.sections_tree = ttk.Treeview(
            self.frame,
            columns=("ID", "Name", "Description"),
            show="headings"
        )
        self.sections_tree.heading("ID", text="ID")
        self.sections_tree.heading("Name", text="Название участка")
        self.sections_tree.heading("Description", text="Описание")
        self.sections_tree.pack(expand=True, fill="both", padx=10, pady=10)

        # Кнопка для создания задания на смену
        Button(self.frame, text="Создать задание на смену", command=self.open_create_shift_task_form).pack(pady=10)

    def load_free_sections(self):
        """Загружает список свободных участков на выбранную дату."""
        selected_date = self.date_entry.get().strip()
        try:
            # Проверка формата даты
            datetime.datetime.strptime(selected_date, "%Y-%m-%d")

            # Получение свободных участков
            free_sections = self.get_free_sections(selected_date)

            # Очищаем таблицу перед загрузкой
            for item in self.sections_tree.get_children():
                self.sections_tree.delete(item)

            # Заполняем таблицу данными
            if free_sections:
                for section in free_sections:
                    self.sections_tree.insert("", "end", values=section)
            else:
                messagebox.showinfo("Результат", "На выбранную дату нет свободных участков.")
        except ValueError:
            messagebox.showerror("Ошибка", "Введите дату в формате YYYY-MM-DD.")

    def open_create_shift_task_form(self):
        """Открывает форму для создания задания на смену."""
        selected_item = self.sections_tree.selection()
        if not selected_item:
            messagebox.showwarning("Ошибка", "Выберите свободный участок!")
            return

        selected_section = self.sections_tree.item(selected_item, "values")
        section_id, section_name = selected_section[0], selected_section[1]
        selected_date = self.date_entry.get().strip()

        form = Toplevel(self.frame)
        form.title("Создать задание на смену")
        form.geometry("400x600")

        # Поле "Дата создания"
        Label(form, text="Дата создания").pack(pady=5)
        creation_date = datetime.date.today().strftime("%Y-%m-%d")
        Label(form, text=creation_date).pack(pady=5)

        # Поле "Смена"
        Label(form, text="Смена (дата)").pack(pady=5)
        Label(form, text=selected_date).pack(pady=5)

        # Поле "Рабочий участок"
        Label(form, text="Рабочий участок").pack(pady=5)
        Label(form, text=section_name).pack(pady=5)

        # Поле "Задание на производство"
        Label(form, text="Задание на производство").pack(pady=5)
        production_tasks = self.get_production_tasks(section_id)
        production_tasks_combobox = ttk.Combobox(form, state="readonly", values=[f"{t[0]}: {t[1]}" for t in production_tasks])
        production_tasks_combobox.pack(pady=5, fill="x", padx=10)

        # Поля "Тип продукции" и "Количество"
        Label(form, text="Тип продукции").pack(pady=5)
        product_label = Label(form, text="")
        product_label.pack(pady=5)

        Label(form, text="Количество").pack(pady=5)
        quantity_label = Label(form, text="")
        quantity_label.pack(pady=5)

        # Поле "Дополнительное описание"
        Label(form, text="Дополнительное описание").pack(pady=5)
        additional_info_text = Text(form, height=5)
        additional_info_text.pack(pady=5, fill="both", padx=10)

        def update_product_info(event):
            """Обновляет информацию о типе продукции и количестве."""
            selected_task = production_tasks_combobox.get()
            if selected_task:
                task_id = int(selected_task.split(":")[0])
                product_id, quantity = next((t[2], t[3]) for t in production_tasks if t[0] == task_id)
                product_label.config(text=product_id)
                quantity_label.config(text=quantity)

        production_tasks_combobox.bind("<<ComboboxSelected>>", update_product_info)

        def save_task():
            """Сохраняет задание на смену."""
            selected_task = production_tasks_combobox.get()
            if not selected_task:
                messagebox.showerror("Ошибка", "Выберите задание на производство!")
                return

            additional_info = additional_info_text.get("1.0", "end").strip()
            task_id = int(selected_task.split(":")[0])

            try:
                conn = connect_db()
                cursor = conn.cursor()
                # Сохранение задания на смену
                cursor.execute("""
                    INSERT INTO shift_tasks (creation_date, production_task_id, shift_date, section_name, additional_info)
                    VALUES (?, ?, ?, ?, ?)
                """, (creation_date, task_id, selected_date, section_name, additional_info))

                # Резервирование участка
                cursor.execute("""
                    INSERT INTO section_availability (section_id, date)
                    VALUES (?, ?)
                """, (section_id, selected_date))

                conn.commit()
                messagebox.showinfo("Успех", "Задание на смену создано!")
                form.destroy()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при сохранении задания: {e}")
            finally:
                conn.close()

        Button(form, text="Сохранить", command=save_task).pack(pady=10)

    @staticmethod
    def get_free_sections(date):
        """Получает список свободных участков на указанную дату."""
        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT s.id, s.name, s.description
                FROM sections s
                WHERE s.id NOT IN (
                    SELECT section_id
                    FROM section_availability
                    WHERE date = ?
                )
            """, (date,))
            return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def get_production_tasks(section_id):
        """Возвращает список заданий на производство для указанного участка."""
        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT pt.id, pt.additional_info, pt.product_id, pt.quantity
                FROM production_tasks pt
                JOIN sections s ON pt.workshops LIKE '%' || s.workshop_id || '%'
                WHERE s.id = ?
            """, (section_id,))
            return cursor.fetchall()
        finally:
            conn.close()

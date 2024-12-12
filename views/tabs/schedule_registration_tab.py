from tkinter import ttk, Toplevel, Label, Entry, Button, Listbox, MULTIPLE, messagebox
from db import connect_db
import datetime


class ScheduleRegistrationTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.setup_tab()

    def setup_tab(self):
        """Настройка вкладки."""
        Label(self.frame, text="Список зарегистрированных расписаний:").pack(pady=10)

        # Таблица для отображения расписаний
        self.schedule_tree = ttk.Treeview(
            self.frame,
            columns=("ID", "Brigade Type", "Section", "Start Date", "Work Mode", "Members", "Master"),
            show="headings"
        )
        self.schedule_tree.heading("ID", text="ID")
        self.schedule_tree.heading("Brigade Type", text="Вид бригады")
        self.schedule_tree.heading("Section", text="Рабочий участок")
        self.schedule_tree.heading("Start Date", text="Дата начала")
        self.schedule_tree.heading("Work Mode", text="Режим работы")
        self.schedule_tree.heading("Members", text="Состав")
        self.schedule_tree.heading("Master", text="Мастер")
        self.schedule_tree.pack(expand=True, fill="both", padx=10, pady=10)

        # Кнопка для регистрации расписания
        Button(self.frame, text="Создать расписание", command=self.open_registration_form).pack(pady=10)

        # Загрузка данных
        self.load_schedules()

    def load_schedules(self):
        """Загружает список расписаний."""
        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT 
                    s.id, bt.name, sec.name, s.start_date, s.work_mode, s.members, s.master
                FROM brigade_schedule s
                JOIN brigade_types bt ON s.brigade_type_id = bt.id
                JOIN sections sec ON s.section_id = sec.id
            """)
            rows = cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить расписания: {e}")
            rows = []
        finally:
            conn.close()

        # Очищаем таблицу
        for item in self.schedule_tree.get_children():
            self.schedule_tree.delete(item)

        # Заполняем таблицу данными
        for row in rows:
            self.schedule_tree.insert("", "end", values=row)

    def open_registration_form(self):
        """Открывает форму регистрации расписания."""
        form = Toplevel(self.frame)
        form.title("Регистрация расписания бригады")
        form.geometry("500x600")

        # Дата создания
        creation_date = datetime.date.today().strftime("%Y-%m-%d")

        # Вид бригады
        Label(form, text="Вид бригады:").pack(pady=5)
        brigade_type_combobox = ttk.Combobox(form, state="readonly")
        brigade_type_combobox.pack(pady=5, fill="x")
        brigade_type_combobox.bind("<<ComboboxSelected>>", lambda e: self.load_sections_for_brigade(
            brigade_type_combobox.get().split(" - ")[0], section_combobox
        ))

        # Рабочий участок
        Label(form, text="Рабочий участок:").pack(pady=5)
        section_combobox = ttk.Combobox(form, state="readonly")
        section_combobox.pack(pady=5, fill="x")

        # Дата начала
        Label(form, text="Дата начала работы:").pack(pady=5)
        start_date_entry = Entry(form)
        start_date_entry.pack(pady=5, fill="x")

        # Режим работы
        Label(form, text="Режим работы:").pack(pady=5)
        work_mode_combobox = ttk.Combobox(form, state="readonly")
        work_mode_combobox["values"] = ["1/1", "2/2"]
        work_mode_combobox.pack(pady=5, fill="x")

        # Состав бригады
        Label(form, text="Состав бригады:").pack(pady=5)
        employees_listbox = Listbox(form, selectmode=MULTIPLE)
        employees_listbox.pack(pady=5, fill="both", expand=True)

        # Мастер
        Label(form, text="Мастер (выберите из сотрудников):").pack(pady=5)
        master_combobox = ttk.Combobox(form, state="readonly")
        master_combobox.pack(pady=5, fill="x")

        # Привязка обновления мастера при выборе сотрудников
        employees_listbox.bind("<<ListboxSelect>>", lambda e: self.update_master_list(employees_listbox, master_combobox))

        # Кнопка для сохранения
        Button(form, text="Сохранить расписание", command=lambda: self.save_schedule(
            form, brigade_type_combobox, section_combobox, start_date_entry, work_mode_combobox,
            employees_listbox, master_combobox, creation_date
        )).pack(pady=10)

        # Загрузка данных для формы
        self.load_brigade_types(brigade_type_combobox)
        self.load_employees(employees_listbox)

    def load_brigade_types(self, combobox):
        """Загружает виды бригад в выпадающий список."""
        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, name FROM brigade_types")
            combobox["values"] = [f"{row[0]} - {row[1]}" for row in cursor.fetchall()]
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить виды бригад: {e}")
        finally:
            conn.close()

    def load_sections_for_brigade(self, brigade_type_id, combobox):
        """Загружает рабочие участки для выбранного вида бригады."""
        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT s.id, s.name
                FROM sections s
                JOIN workshops w ON w.id = s.workshop_id
                WHERE w.id = (
                    SELECT bt.id FROM brigade_types bt WHERE bt.id = ?
                )
            """, (brigade_type_id,))
            sections = cursor.fetchall()
            if sections:
                combobox["values"] = [f"{row[0]} - {row[1]}" for row in sections]
            else:
                combobox["values"] = []
                messagebox.showinfo("Информация", "Нет доступных участков для выбранного вида бригады.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить участки: {e}")
        finally:
            conn.close()

    def load_employees(self, listbox):
        """Загружает сотрудников в список."""
        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, full_name FROM employees")
            employees = cursor.fetchall()
            listbox.delete(0, "end")
            for emp in employees:
                listbox.insert("end", f"{emp[0]} - {emp[1]}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить сотрудников: {e}")
        finally:
            conn.close()

    def update_master_list(self, employees_listbox, master_combobox):
        """Обновляет список мастеров на основе выбранных сотрудников."""
        selected_employees = [employees_listbox.get(i) for i in employees_listbox.curselection()]
        master_combobox["values"] = selected_employees
        if master_combobox.get() not in selected_employees and selected_employees:
            master_combobox.set(selected_employees[0])  # Устанавливаем первого выбранного сотрудника как мастера по умолчанию

    def save_schedule(self, form, brigade_combobox, section_combobox, start_date_entry, work_mode_combobox, employees_listbox, master_combobox, creation_date):
        """Сохраняет расписание в базу данных."""
        # Собираем данные
        brigade_type = brigade_combobox.get()
        section = section_combobox.get()
        start_date = start_date_entry.get()
        work_mode = work_mode_combobox.get()
        selected_employees = [employees_listbox.get(i) for i in employees_listbox.curselection()]
        master = master_combobox.get()

        # Валидация
        if not brigade_type or not section or not start_date or not work_mode or not selected_employees or not master:
            messagebox.showerror("Ошибка", "Все поля обязательны для заполнения!")
            return

        # Проверка даты начала работы
        try:
            start_date_obj = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
            creation_date_obj = datetime.datetime.strptime(creation_date, "%Y-%m-%d").date()
            if start_date_obj < creation_date_obj:
                messagebox.showerror("Ошибка", "Дата начала работы не может быть раньше даты создания!")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Введите дату начала работы в формате YYYY-MM-DD!")
            return

        # Проверка уникальности сотрудников
        try:
            conn = connect_db()
            cursor = conn.cursor()

            # Проверка сотрудников в других бригадах
            employee_ids = [emp.split(" - ")[0] for emp in selected_employees]
            cursor.execute("""
                SELECT DISTINCT s.id
                FROM brigade_schedule s
                WHERE s.members LIKE ?
                AND s.start_date = ?
            """, ("%{}%".format(employee_ids[0]), start_date))
            existing_employees = cursor.fetchall()
            if existing_employees:
                messagebox.showerror("Ошибка", "Некоторые сотрудники уже задействованы в другой бригаде на указанную дату!")
                return
        finally:
            conn.close()

        # Сохранение данных
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO brigade_schedule (brigade_type_id, section_id, start_date, work_mode, members, master)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (brigade_type.split(" - ")[0], section.split(" - ")[0], start_date, work_mode,
                  ", ".join(selected_employees), master.split(" - ")[1]))
            conn.commit()
            messagebox.showinfo("Успех", "Расписание успешно создано!")
            form.destroy()
            self.load_schedules()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить расписание: {e}")
        finally:
            conn.close()

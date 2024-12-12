from tkinter import ttk, messagebox, Toplevel, Label, Entry, Text
from db import connect_db
import datetime


class ShiftTasksTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        parent.add(self.frame, text="Задания на производство")
        self.setup_tab()

    def setup_tab(self):
        """Настраивает вкладку."""
        # Заголовок для таблицы "Задания на производство"
        ttk.Label(self.frame, text="Список заданий на производство").pack(pady=5)

        # Таблица для отображения заданий на производство
        self.tasks_tree = ttk.Treeview(
            self.frame,
            columns=("ID", "Registration Date", "Start Date", "Order ID", "Product ID", "Quantity", "Workshops", "Additional Info"),
            show="headings",
        )
        self.tasks_tree.heading("ID", text="ID")
        self.tasks_tree.heading("Registration Date", text="Дата регистрации")
        self.tasks_tree.heading("Start Date", text="Дата начала")
        self.tasks_tree.heading("Order ID", text="ID заказа")
        self.tasks_tree.heading("Product ID", text="Продукция")
        self.tasks_tree.heading("Quantity", text="Количество")
        self.tasks_tree.heading("Workshops", text="Цеха")
        self.tasks_tree.heading("Additional Info", text="Доп. информация")
        self.tasks_tree.pack(expand=True, fill="both", padx=10, pady=5)

        # Кнопка для регистрации задания на смену
        ttk.Button(self.frame, text="Зарегистрировать задание на смену", command=self.open_shift_task_form).pack(pady=10)

        # Заголовок для таблицы "Задания на смену"
        ttk.Label(self.frame, text="Список заданий на смену").pack(pady=5)

        # Таблица для отображения заданий на смену
        self.shift_tasks_tree = ttk.Treeview(
            self.frame,
            columns=("ID", "Creation Date", "Production Task ID", "Shift Date", "Section Name", "Additional Info"),
            show="headings",
        )
        self.shift_tasks_tree.heading("ID", text="ID")
        self.shift_tasks_tree.heading("Creation Date", text="Дата создания")
        self.shift_tasks_tree.heading("Production Task ID", text="ID задания на производство")
        self.shift_tasks_tree.heading("Shift Date", text="Дата смены")
        self.shift_tasks_tree.heading("Section Name", text="Участок")
        self.shift_tasks_tree.heading("Additional Info", text="Доп. информация")
        self.shift_tasks_tree.pack(expand=True, fill="both", padx=10, pady=5)

        # Загрузка данных
        self.load_production_tasks()
        self.load_shift_tasks()

    def load_production_tasks(self):
        """Загружает задания на производство из базы данных."""
        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT id, registration_date, start_date, order_id, product_id, quantity, workshops, additional_info
                FROM production_tasks
            """)
            rows = cursor.fetchall()
        except Exception as e:
            print(f"Ошибка загрузки данных: {e}")
            rows = []
        finally:
            conn.close()

        # Очищаем таблицу перед загрузкой
        for item in self.tasks_tree.get_children():
            self.tasks_tree.delete(item)

        # Заполняем таблицу данными
        for row in rows:
            self.tasks_tree.insert("", "end", values=row)

    def load_shift_tasks(self):
        """Загружает задания на смену из базы данных."""
        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT id, creation_date, production_task_id, shift_date, section_name, additional_info
                FROM shift_tasks
            """)
            rows = cursor.fetchall()
        except Exception as e:
            print(f"Ошибка загрузки данных: {e}")
            rows = []
        finally:
            conn.close()

        # Очищаем таблицу перед загрузкой
        for item in self.shift_tasks_tree.get_children():
            self.shift_tasks_tree.delete(item)

        # Заполняем таблицу данными
        for row in rows:
            self.shift_tasks_tree.insert("", "end", values=row)

    def open_shift_task_form(self):
        """Открывает форму для регистрации задания на смену."""
        selected_item = self.tasks_tree.selection()
        if not selected_item:
            messagebox.showwarning("Ошибка", "Выберите задание на производство!")
            return

        production_task_data = self.tasks_tree.item(selected_item, "values")
        production_task_id, registration_date, start_date, order_id, product_id, quantity, workshops, additional_info = production_task_data

        form = Toplevel(self.frame)
        form.title("Регистрация задания на смену")
        form.geometry("400x600")

        # Поле "Дата создания"
        Label(form, text="Дата создания").pack(pady=5)
        creation_date = datetime.date.today().strftime("%Y-%m-%d")
        creation_date_label = Label(form, text=creation_date)
        creation_date_label.pack(pady=5)

        # Поле "Тип продукции"
        Label(form, text="Тип продукции").pack(pady=5)
        product_label = Label(form, text=product_id)  # Поле product_id - это название продукции
        product_label.pack(pady=5)

        # Поле "Количество"
        Label(form, text="Количество").pack(pady=5)
        quantity_label = Label(form, text=quantity)
        quantity_label.pack(pady=5)

        # Поле "Смена"
        Label(form, text="Смена (YYYY-MM-DD)").pack(pady=5)
        shift_date_entry = Entry(form)
        shift_date_entry.pack(pady=5, fill="x", padx=10)

        # Поле "Выбор участка"
        Label(form, text="Выбор участка").pack(pady=5)
        sections_combobox = ttk.Combobox(form, state="readonly")
        sections_combobox.pack(pady=5, fill="x", padx=10)

        def on_date_change(event):
            selected_date = shift_date_entry.get().strip()
            if selected_date:
                self.load_sections_for_date(sections_combobox, selected_date)

        shift_date_entry.bind("<FocusOut>", on_date_change)

        # Поле "Дополнительное описание"
        Label(form, text="Дополнительное описание").pack(pady=5)
        additional_info_text = Text(form, height=5)
        additional_info_text.pack(pady=5, fill="both", padx=10)

        def save_task():
            """Сохраняет задание на смену."""
            shift_date = shift_date_entry.get().strip()
            section_name = sections_combobox.get()
            additional_info = additional_info_text.get("1.0", "end").strip()

            if not shift_date or not section_name:
                messagebox.showerror("Ошибка", "Все поля, кроме дополнительного описания, обязательны для заполнения!")
                return

            try:
                shift_date_obj = datetime.datetime.strptime(shift_date, "%Y-%m-%d").date()
                creation_date_obj = datetime.datetime.strptime(creation_date, "%Y-%m-%d").date()
                start_date_obj = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()

                if not (creation_date_obj <= shift_date_obj <= start_date_obj):
                    messagebox.showerror("Ошибка", "Дата смены должна быть между датой создания и датой начала производства!")
                    return

                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO shift_tasks (creation_date, production_task_id, shift_date, section_name, additional_info)
                    VALUES (?, ?, ?, ?, ?)
                """, (creation_date, production_task_id, shift_date, section_name, additional_info))

                cursor.execute("""
                    INSERT INTO section_availability (section_id, date)
                    VALUES ((SELECT id FROM sections WHERE name = ?), ?)
                """, (section_name, shift_date))
                conn.commit()
                messagebox.showinfo("Успех", "Задание на смену зарегистрировано!")
                self.load_shift_tasks()  # Обновляем таблицу заданий на смену
                form.destroy()
            except ValueError:
                messagebox.showerror("Ошибка", "Введите дату смены в правильном формате YYYY-MM-DD!")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при сохранении задания: {e}")
            finally:
                conn.close()

        ttk.Button(form, text="Сохранить", command=save_task).pack(pady=10)

    def load_sections_for_date(self, combobox, date):
        """Загружает список свободных участков на указанную дату."""
        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT name 
                FROM sections 
                WHERE id NOT IN (
                    SELECT section_id 
                    FROM section_availability 
                    WHERE date = ?
                )
            """, (date,))
            sections = cursor.fetchall()
            combobox["values"] = [s[0] for s in sections]
        except Exception as e:
            print(f"Ошибка загрузки участков: {e}")
        finally:
            conn.close()

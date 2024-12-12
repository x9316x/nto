from tkinter import ttk, Label, Frame, messagebox
from db import connect_db
from datetime import datetime, timedelta


class BrigadeScheduleTab:
    def __init__(self, parent):
        self.frame = Frame(parent)
        self.setup_tab()

    def setup_tab(self):
        """Настройка вкладки."""
        Label(self.frame, text="Календарь работы бригад").pack(pady=10)

        # Фильтры для цеха и сотрудника
        filter_frame = Frame(self.frame)
        filter_frame.pack(pady=10)

        Label(filter_frame, text="Цех:").pack(side="left", padx=5)
        self.workshop_filter = ttk.Combobox(filter_frame, state="readonly")
        self.workshop_filter.pack(side="left", padx=5)
        self.workshop_filter.bind("<<ComboboxSelected>>", lambda e: self.load_schedule())

        Label(filter_frame, text="Сотрудник:").pack(side="left", padx=5)
        self.employee_filter = ttk.Combobox(filter_frame, state="readonly")
        self.employee_filter.pack(side="left", padx=5)
        self.employee_filter.bind("<<ComboboxSelected>>", lambda e: self.load_schedule())

        # Таблица для отображения расписания
        self.schedule_tree = ttk.Treeview(
            self.frame,
            columns=("Date", "Section", "Brigade", "Members", "Shift Task"),
            show="headings"
        )
        self.schedule_tree.heading("Date", text="Дата")
        self.schedule_tree.heading("Section", text="Рабочий участок")
        self.schedule_tree.heading("Brigade", text="Бригада")
        self.schedule_tree.heading("Members", text="Состав")
        self.schedule_tree.heading("Shift Task", text="Задание на смену")
        self.schedule_tree.pack(expand=True, fill="both", padx=10, pady=10)

        # Загрузка данных для фильтров
        self.load_workshops()
        self.load_employees()

        # Загрузка данных расписания
        self.load_schedule()

    def load_workshops(self):
        """Загружает список цехов в фильтр."""
        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, name FROM workshops")
            workshops = cursor.fetchall()
            self.workshop_filter["values"] = ["Все"] + [f"{w[0]} - {w[1]}" for w in workshops]
            self.workshop_filter.set("Все")
        except Exception as e:
            print(f"Ошибка загрузки цехов: {e}")
        finally:
            conn.close()

    def load_employees(self):
        """Загружает список сотрудников в фильтр."""
        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, full_name FROM employees")
            employees = cursor.fetchall()
            self.employee_filter["values"] = ["Все"] + [f"{e[0]} - {e[1]}" for e in employees]
            self.employee_filter.set("Все")
        except Exception as e:
            print(f"Ошибка загрузки сотрудников: {e}")
        finally:
            conn.close()

    def load_schedule(self):
        """Загружает расписание работы бригад."""
        conn = connect_db()
        cursor = conn.cursor()
        try:
            # Очистка таблицы
            for item in self.schedule_tree.get_children():
                self.schedule_tree.delete(item)

            # Формирование запроса для получения расписаний
            query = """
                SELECT
                    bs.start_date,
                    bs.work_mode,
                    sec.name AS section_name,
                    bt.name AS brigade_name,
                    bs.members,
                    st.additional_info AS shift_task
                FROM brigade_schedule bs
                JOIN sections sec ON bs.section_id = sec.id
                JOIN brigade_types bt ON bt.id = bs.brigade_type_id
                LEFT JOIN shift_tasks st ON st.section_name = sec.name
                WHERE 1=1
            """
            params = []

            # Применяем фильтр по цеху
            workshop_filter = self.workshop_filter.get()
            if workshop_filter != "Все":
                workshop_id = workshop_filter.split(" - ")[0]
                query += " AND sec.workshop_id = ?"
                params.append(workshop_id)

            # Применяем фильтр по сотруднику
            employee_filter = self.employee_filter.get()
            if employee_filter != "Все":
                employee_id = employee_filter.split(" - ")[0]
                query += " AND bs.members LIKE ?"
                params.append(f"%{employee_id}%")

            cursor.execute(query, params)
            schedules = cursor.fetchall()

            # Генерация календаря для каждого расписания
            for schedule in schedules:
                start_date = datetime.strptime(schedule[0], "%Y-%m-%d")
                work_mode = schedule[1]
                section_name = schedule[2]
                brigade_name = schedule[3]
                members = schedule[4]
                shift_task = schedule[5]

                # Генерация расписания на месяц
                days_in_month = 30
                work_days, rest_days = map(int, work_mode.split("/"))
                current_date = start_date
                while (current_date - start_date).days < days_in_month:
                    # Рабочие дни
                    for _ in range(work_days):
                        if (current_date - start_date).days >= days_in_month:
                            break
                        self.schedule_tree.insert("", "end", values=(
                            current_date.strftime("%Y-%m-%d"),
                            section_name,
                            brigade_name,
                            members,
                            shift_task
                        ))
                        current_date += timedelta(days=1)

                    # Дни отдыха
                    current_date += timedelta(days=rest_days)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить расписание: {e}")
        finally:
            conn.close()

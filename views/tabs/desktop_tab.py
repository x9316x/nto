from tkinter import ttk, StringVar, messagebox
from db import connect_db


class DesktopTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        parent.add(self.frame, text="Рабочий стол")
        self.selected_workshop = StringVar()  # Для фильтрации по цеху

        self.setup_tab()

    def setup_tab(self):
        """Настраивает вкладку рабочего стола."""
        # Заголовок
        ttk.Label(self.frame, text="Рабочий стол - Задания на подготовку").pack(pady=5)

        # Выпадающий список для фильтрации по цеху
        filter_frame = ttk.Frame(self.frame)
        filter_frame.pack(pady=5, padx=10, fill="x")

        ttk.Label(filter_frame, text="Выберите цех:").pack(side="left", padx=5)
        self.workshop_combobox = ttk.Combobox(
            filter_frame, textvariable=self.selected_workshop, state="readonly"
        )
        self.workshop_combobox.pack(side="left", fill="x", expand=True, padx=5)

        ttk.Button(filter_frame, text="Применить фильтр", command=self.load_tasks).pack(side="left", padx=5)

        # Таблица для отображения заданий
        self.tree = ttk.Treeview(
            self.frame,
            columns=("ID", "Required Date", "Section", "Description", "Status"),
            show="headings",
        )
        self.tree.heading("ID", text="ID")
        self.tree.heading("Required Date", text="Дата подготовки")
        self.tree.heading("Section", text="Название участка")
        self.tree.heading("Description", text="Описание")
        self.tree.heading("Status", text="Статус")
        self.tree.pack(expand=True, fill="both", padx=10, pady=5)

        # Загрузка данных
        self.load_workshops()
        self.load_tasks()

    def load_workshops(self):
        """Загружает список цехов для фильтрации."""
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM workshops")
        workshops = cursor.fetchall()
        conn.close()

        # Устанавливаем значения в выпадающий список
        self.workshop_combobox["values"] = [w[0] for w in workshops]
        if workshops:
            self.selected_workshop.set(workshops[0][0])  # Устанавливаем первый цех как выбранный

    def load_tasks(self):
        """Загружает задания из таблицы preparation_tasks со статусом 'Создано'."""
        selected_workshop = self.selected_workshop.get()

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT pt.id, pt.required_date, s.name, s.description, pt.status
            FROM preparation_tasks pt
            JOIN sections s ON pt.section_id = s.id
            JOIN workshops w ON s.workshop_id = w.id
            WHERE pt.status = 'Создано' AND w.name = ?
        """, (selected_workshop,))
        tasks = cursor.fetchall()
        conn.close()

        # Очищаем таблицу перед загрузкой
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Заполняем таблицу данными
        for task in tasks:
            self.tree.insert("", "end", values=task)

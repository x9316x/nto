from tkinter import ttk
from tkinter import simpledialog, messagebox
from db import connect_db

class ProductsTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        parent.add(self.frame, text="Виды лесопродукции")
        self.setup_tab()

    def setup_tab(self):
        """Настраивает вкладку."""
        ttk.Label(self.frame, text="Список видов лесопродукции").pack(pady=10)

        # Таблица
        self.tree = ttk.Treeview(self.frame, columns=("ID", "Name"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Название")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        # Кнопки управления
        buttons_frame = ttk.Frame(self.frame)
        buttons_frame.pack(pady=10)

        ttk.Button(buttons_frame, text="Добавить", command=self.add_product).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Удалить", command=self.delete_product).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Редактировать", command=self.edit_product).pack(side="left", padx=5)

        # Загрузка данных
        self.load_products()

    def load_products(self):
        """Загружает данные о видах лесопродукции из базы."""
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM products")
        rows = cursor.fetchall()
        conn.close()

        # Очищаем таблицу перед загрузкой
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Заполняем таблицу данными
        for row in rows:
            self.tree.insert("", "end", values=row)

    def add_product(self):
        """Добавляет новый вид лесопродукции."""
        product_name = simpledialog.askstring("Добавить продукт", "Введите название продукции:")
        if not product_name:
            return

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (name) VALUES (?)", (product_name,))
        conn.commit()
        conn.close()

        self.load_products()
        messagebox.showinfo("Успех", f"Продукция '{product_name}' добавлена!")

    def delete_product(self):
        """Удаляет выбранный вид лесопродукции."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Ошибка", "Выберите продукцию для удаления!")
            return

        product_id = self.tree.item(selected_item, "values")[0]
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        conn.commit()
        conn.close()

        self.load_products()
        messagebox.showinfo("Успех", f"Продукция с ID {product_id} удалена!")

    def edit_product(self):
        """Редактирует выбранный вид лесопродукции."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Ошибка", "Выберите продукцию для редактирования!")
            return

        product_id, product_name = self.tree.item(selected_item, "values")
        new_name = simpledialog.askstring("Редактировать продукт", "Введите новое название продукции:", initialvalue=product_name)

        if not new_name:
            return

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE products SET name = ? WHERE id = ?", (new_name, product_id))
        conn.commit()
        conn.close()

        self.load_products()
        messagebox.showinfo("Успех", f"Продукция с ID {product_id} обновлена на '{new_name}'!")

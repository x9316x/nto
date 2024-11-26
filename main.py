import tkinter as tk
from tkinter import ttk
from views.commercial_window import CommercialServiceWindow
from views.production_view import ProductionServiceWindow
from views.tech_view import TechServiceWindow
from db import create_tables
from models import insert_initial_data
import os
import sys

def center_window(window):
    """Центрирует окно на экране с учётом его текущего размера."""
    window.update_idletasks()  # Обновляем размеры окна
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

# Главное окно
root = tk.Tk()

# Функции для открытия служб
def open_commercial_service():
    window = CommercialServiceWindow(root)
    center_window(window.window)  # Центрируем дочернее окно
    window.window.resizable(True, True)  # Разрешаем изменение размера

def open_production_service():
    window = ProductionServiceWindow(root)
    center_window(window.window)  # Центрируем дочернее окно
    window.window.resizable(True, True)  # Разрешаем изменение размера

def open_tech_service():
    window = TechServiceWindow(root)
    center_window(window.window)  # Центрируем дочернее окно
    window.window.resizable(True, True)  # Разрешаем изменение размера

def main():
    # Инициализация базы данных
    create_tables()  # Создаём таблицы
    insert_initial_data()  # Добавляем тестовые данные (если их нет)

    # Настройка главного окна
    root.title("Система управления Лесозаводом №10")
    center_window(root)  # Центрируем главное окно
    root.resizable(True, True)  # Разрешаем изменение размера

    # Настройка растягивания
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Заголовок
    label = ttk.Label(root, text="Выберите службу", font=("Arial", 14))
    label.pack(pady=20)

    # Кнопки служб
    ttk.Button(root, text="Коммерческая служба", command=open_commercial_service).pack(pady=10)
    ttk.Button(root, text="Служба производства", command=open_production_service).pack(pady=10)
    ttk.Button(root, text="Служба технолога", command=open_tech_service).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()

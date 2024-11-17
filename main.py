import tkinter as tk
from tkinter import ttk
from views.commercial_window import CommercialServiceWindow
from views.production_view import ProductionServiceWindow
from views.tech_view import TechServiceWindow

# Главное окно
root = tk.Tk()

# Функции для открытия служб
def open_commercial_service():
    CommercialServiceWindow(root)

def open_production_service():
    ProductionServiceWindow(root)  # Полный функционал

def open_tech_service():
    TechServiceWindow(root)  # Полный функционал

def main():
    # Настройка главного окна
    root.title("Система управления Лесозаводом №10")
    root.geometry("400x300")

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

"""Главное окно приложения с каталогом."""
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from config import APP_TITLE, FONT_FAMILY, COLOR_SECONDARY
import database as db
from catalog import create_product_card


class CatalogWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        self.root.geometry("900x700")
        try:
            self.root.iconbitmap("resources/icon.ico")
        except tk.TclError:
            pass

        self.build_ui()
        self.load_products()

    def build_ui(self):
        # Заголовок
        header = tk.Frame(self.root, bg=COLOR_SECONDARY)
        header.pack(fill="x")

        # Логотип слева в шапке
        try:
            logo = Image.open("resources/logo.png").resize((50, 50))
            self.logo_photo = ImageTk.PhotoImage(logo)   # ссылка, чтобы не удалил сборщик мусора
            tk.Label(header, image=self.logo_photo, bg=COLOR_SECONDARY).pack(side="left", padx=10, pady=5)
        except OSError:
            pass

        tk.Label(header, text="КАТАЛОГ ТОВАРОВ",
                 font=(FONT_FAMILY, 16, "bold"),
                 bg=COLOR_SECONDARY).pack(side="left", pady=15)

        # Область с прокруткой
        self.canvas = tk.Canvas(self.root, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical",
                                  command=self.canvas.yview)
        self.catalog_frame = tk.Frame(self.canvas, bg="white")
        self.catalog_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        window = self.canvas.create_window((0, 0), window=self.catalog_frame, anchor="nw")
        # карточки растягиваются на всю ширину окна
        self.canvas.bind("<Configure>",
                         lambda e: self.canvas.itemconfigure(window, width=e.width))
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def load_products(self):
        products = db.get_all_products()
        for p in products:
            create_product_card(self.catalog_frame, p)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    CatalogWindow().run()

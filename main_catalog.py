"""Главное окно с каталогом."""
import os
import tkinter as tk
from tkinter import ttk

from styles import COLOR_MAIN_BG, COLOR_SECONDARY_BG, FONT_SIZE_TITLE, font
from config import APP_TITLE
import database as db
from catalog import create_product_card
from resources import load_image_proportional, PATH_LOGO, PATH_ICON


def set_app_icon(root, icon_path):
    """Устанавливает иконку приложения кроссплатформенно."""
    try:
        if os.name == "nt":   # Windows
            if os.path.exists(icon_path):
                root.iconbitmap(icon_path)
        else:                  # Linux/Mac
            png_path = icon_path.replace(".ico", ".png")
            icon_img = load_image_proportional(png_path, max_size=(32, 32))
            if icon_img:
                root.iconphoto(True, icon_img)
                root._icon_photo = icon_img   # сохраняем ссылку
    except Exception as e:
        print(f"Не удалось установить иконку: {e}")


class CatalogWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        self.root.geometry("900x700")
        self.root.configure(bg=COLOR_MAIN_BG)

        # Иконка приложения
        set_app_icon(self.root, PATH_ICON)

        self.build_ui()
        self.load_products()

    def build_ui(self):
        # Шапка с логотипом и заголовком
        header = tk.Frame(self.root, bg=COLOR_SECONDARY_BG, height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        # Логотип (слева) — с сохранением пропорций!
        logo = load_image_proportional(PATH_LOGO, max_size=(60, 60))
        if logo:
            self.logo_label = tk.Label(header, image=logo, bg=COLOR_SECONDARY_BG)
            self.logo_label.image = logo
            self.logo_label.pack(side="left", padx=15)
        else:
            tk.Label(header, text="[ЛОГОТИП]",
                     bg=COLOR_SECONDARY_BG).pack(side="left", padx=15)

        # Заголовок (по центру)
        tk.Label(header, text="КАТАЛОГ ТОВАРОВ",
                 font=font(FONT_SIZE_TITLE, bold=True),
                 bg=COLOR_SECONDARY_BG).pack(expand=True)

        # Область с прокруткой
        self.canvas = tk.Canvas(self.root, bg=COLOR_MAIN_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical",
                                  command=self.canvas.yview)
        self.catalog_frame = tk.Frame(self.canvas, bg=COLOR_MAIN_BG)
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

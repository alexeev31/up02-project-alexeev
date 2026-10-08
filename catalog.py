"""Каталог товаров."""
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from PIL import Image, ImageTk
import os

from config import (DB_PATH, COLOR_HIGHLIGHT, FONT_FAMILY,
                    RESOURCES_DIR, PLACEHOLDER_IMAGE)
from discount import calculate_price_with_discount
import database as db


def create_product_card(parent, product):
    """
    Создаёт карточку товара по макету.

    :param parent: родительский контейнер
    :param product: кортеж из БД
        (id, категория, название, вес, цена, количество, фото, состав)
    """
    # Определяем фон: подсветка, если количество ≤3
    qty = product[5]
    bg_color = COLOR_HIGHLIGHT if qty <= 3 else "white"

    # Карточка без рамки, снизу — разделитель (вариант 2 макета)
    card = tk.Frame(parent, bg=bg_color)
    card.pack(fill="x", padx=10, pady=(5, 0))
    ttk.Separator(parent, orient="horizontal").pack(fill="x", padx=10, pady=(5, 0))

    # === Изображение (слева) ===
    img_frame = tk.Frame(card, bg=bg_color)
    img_frame.pack(side="left", padx=10, pady=10)

    image_path = os.path.join(RESOURCES_DIR, product[6]) if product[6] else PLACEHOLDER_IMAGE
    if not os.path.exists(image_path):
        image_path = PLACEHOLDER_IMAGE

    try:
        img = Image.open(image_path).resize((100, 100))
        photo = ImageTk.PhotoImage(img)
        img_label = tk.Label(img_frame, image=photo, bg=bg_color)
        img_label.image = photo   # сохраняем ссылку!
        img_label.pack()
    except Exception:
        tk.Label(img_frame, text="[ФОТО]", bg=bg_color,
                 width=10, height=5).pack()

    # === Цена (справа) ===
    price = product[4]
    new_price = calculate_price_with_discount(product[0], price, datetime.now())
    price_frame = tk.Frame(card, bg=bg_color)
    price_frame.pack(side="right", padx=15, pady=10)
    if new_price != price:
        # старая цена зачёркнута, новая — со скидкой
        tk.Label(price_frame, text=f"{price:g} руб.", fg="red",
                 font=(FONT_FAMILY, 11, "overstrike"), bg=bg_color).pack(anchor="e")
    tk.Label(price_frame, text=f"{new_price:g} руб.",
             font=(FONT_FAMILY, 14, "bold"), bg=bg_color).pack(anchor="e")

    # === Текстовая часть (между фото и ценой) ===
    text_frame = tk.Frame(card, bg=bg_color)
    text_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    # Название | вес (поля «Производство» в варианте 4 нет)
    title = f"{product[2]} | {product[3]} г"
    tk.Label(text_frame, text=title, font=(FONT_FAMILY, 14, "bold"),
             bg=bg_color, anchor="w").pack(fill="x")

    # Категория
    tk.Label(text_frame, text=f"Категория: {product[1]}",
             font=(FONT_FAMILY, 11), bg=bg_color, anchor="w").pack(fill="x")

    # Количество
    indicator = "много" if qty > 5 else "мало"
    tk.Label(text_frame, text=f"Количество: {indicator} ({qty})",
             font=(FONT_FAMILY, 11), bg=bg_color, anchor="w").pack(fill="x")

    # Состав
    tk.Label(text_frame, text=f"Состав: {product[7]}",
             font=(FONT_FAMILY, 11), bg=bg_color, anchor="w").pack(fill="x")

    return card

"""Каталог товаров."""
import tkinter as tk
from tkinter import ttk
from datetime import datetime

from styles import (
    COLOR_MAIN_BG, COLOR_HIGHLIGHT,
    FONT_SIZE_NORMAL, FONT_SIZE_HEADER,
    font
)
from resources import get_product_image
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
    bg_color = COLOR_HIGHLIGHT if qty <= 3 else COLOR_MAIN_BG

    # Карточка без рамки, снизу — разделитель (вариант 2 макета)
    card = tk.Frame(parent, bg=bg_color)
    card.pack(fill="x", padx=10, pady=(5, 0))
    ttk.Separator(parent, orient="horizontal").pack(fill="x", padx=10, pady=(5, 0))

    # === Изображение (слева) ===
    img_frame = tk.Frame(card, bg=bg_color)
    img_frame.pack(side="left", padx=10, pady=10)

    photo = get_product_image(product[6], size=(100, 100))
    if photo:
        img_label = tk.Label(img_frame, image=photo, bg=bg_color)
        img_label.image = photo   # сохраняем ссылку!
        img_label.pack()
    else:
        tk.Label(img_frame, text="[НЕТ ФОТО]", bg=bg_color,
                 width=10, height=5).pack()

    # === Цена (справа) ===
    price = product[4]
    new_price = calculate_price_with_discount(product[0], price, datetime.now())
    price_frame = tk.Frame(card, bg=bg_color)
    price_frame.pack(side="right", padx=15, pady=10)
    if new_price != price:
        # старая цена зачёркнута, новая — со скидкой
        old_font = font(FONT_SIZE_NORMAL) + ("overstrike",)
        tk.Label(price_frame, text=f"{price:g} руб.", fg="red",
                 font=old_font, bg=bg_color).pack(anchor="e")
    tk.Label(price_frame, text=f"{new_price:g} руб.",
             font=font(FONT_SIZE_HEADER, bold=True), bg=bg_color).pack(anchor="e")

    # === Текстовая часть (между фото и ценой) ===
    text_frame = tk.Frame(card, bg=bg_color)
    text_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    # Название | вес (поля «Производство» в варианте 4 нет)
    title = f"{product[2]} | {product[3]} г"
    tk.Label(text_frame, text=title, font=font(FONT_SIZE_HEADER, bold=True),
             bg=bg_color, anchor="w").pack(fill="x")

    tk.Label(text_frame, text=f"Категория: {product[1]}",
             font=font(FONT_SIZE_NORMAL), bg=bg_color, anchor="w").pack(fill="x")

    indicator = "много" if qty > 5 else "мало"
    tk.Label(text_frame, text=f"Количество: {indicator} ({qty})",
             font=font(FONT_SIZE_NORMAL), bg=bg_color, anchor="w").pack(fill="x")

    tk.Label(text_frame, text=f"Состав: {product[7]}",
             font=font(FONT_SIZE_NORMAL), bg=bg_color, anchor="w").pack(fill="x")

    return card

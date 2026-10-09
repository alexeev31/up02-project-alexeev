"""Каталог товаров.

Индексы полей товара (вариант 4):
    0 id, 1 категория, 2 название, 3 вес, 4 цена, 5 количество, 6 фото, 7 состав
"""
import tkinter as tk
from tkinter import ttk
from datetime import datetime

from styles import (
    COLOR_MAIN_BG, COLOR_HIGHLIGHT,
    FONT_SIZE_NORMAL, FONT_SIZE_HEADER, font
)
from resources import get_product_image
from discount import calculate_price_with_discount


def create_product_card(parent, product):
    """Создаёт карточку товара по макету."""
    qty = product[5] if product[5] is not None else 0
    bg_color = _get_card_color(qty)

    # Карточка без рамки, снизу — разделитель (вариант 2 макета)
    card = tk.Frame(parent, bg=bg_color)
    card.pack(fill="x", padx=10, pady=(5, 0))
    ttk.Separator(parent, orient="horizontal").pack(fill="x", padx=10, pady=(5, 0))

    _add_image(card, product, bg_color)
    _add_price(card, product, bg_color)
    _add_text_info(card, product, bg_color, qty)

    return card


def _get_card_color(qty):
    """Возвращает цвет фона карточки."""
    return COLOR_HIGHLIGHT if qty <= 3 else COLOR_MAIN_BG


def _indicator(qty):
    """Индикатор «много/мало» (порог 5)."""
    return "много" if qty > 5 else "мало"


def _add_label(parent, text, bg_color, bold=False,
               size=FONT_SIZE_NORMAL, align="w"):
    """Добавляет метку с текстом."""
    tk.Label(parent, text=text, font=font(size, bold=bold),
             bg=bg_color, anchor=align).pack(fill="x")


def _add_image(card, product, bg_color):
    """Добавляет изображение товара (или заглушку)."""
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


def _add_price(card, product, bg_color):
    """Цена справа; если есть скидка — старая цена зачёркнута."""
    price = product[4] if product[4] is not None else 0
    new_price = calculate_price_with_discount(product[0], price, datetime.now())

    price_frame = tk.Frame(card, bg=bg_color)
    price_frame.pack(side="right", padx=15, pady=10)
    if new_price != price:
        tk.Label(price_frame, text=f"{price:g} руб.", fg="red",
                 font=font(FONT_SIZE_NORMAL) + ("overstrike",),
                 bg=bg_color).pack(anchor="e")
    _add_label(price_frame, f"{new_price:g} руб.", bg_color,
               bold=True, size=FONT_SIZE_HEADER, align="e")


def _add_text_info(card, product, bg_color, qty):
    """Добавляет текстовую информацию о товаре."""
    text_frame = tk.Frame(card, bg=bg_color)
    text_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    # Проверка значений (крайние случаи)
    name = product[2] if product[2] else "[Без названия]"
    weight = f"{product[3]} г" if product[3] else "[вес не указан]"
    category = product[1] if product[1] else "[Без категории]"
    composition = product[7] if product[7] else "[Не указан]"

    # «Производство | Наименование» → в варианте 4: «Название | вес»
    _add_label(text_frame, f"{name} | {weight}",
               bg_color, bold=True, size=FONT_SIZE_HEADER)
    _add_label(text_frame, f"Категория: {category}", bg_color)
    _add_label(text_frame, f"Количество: {_indicator(qty)} ({qty})", bg_color)
    _add_label(text_frame, f"Состав: {composition}", bg_color)

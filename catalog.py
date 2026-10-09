"""Каталог товаров."""
import tkinter as tk
from tkinter import ttk
from datetime import datetime

from styles import (
    COLOR_MAIN_BG, COLOR_HIGHLIGHT,
    FONT_FAMILY, FONT_SIZE_NORMAL, FONT_SIZE_HEADER, font
)
from resources import get_product_image
from discount import calculate_price_with_discount

MAX_NAME_LEN = 35


def create_product_card(parent, product):
    """Создаёт карточку товара по макету."""
    qty = product[5]   # вариант 4: количество
    bg_color = _get_card_color(qty)

    card = tk.Frame(parent, bg=bg_color)
    card.pack(fill="x", padx=10, pady=5)
    # разделитель между карточками (ДЗ пары 10)
    ttk.Separator(parent, orient="horizontal").pack(fill="x", padx=10)

    _add_image(card, product, bg_color)
    _add_text_info(card, product, bg_color, qty)

    return card


def _get_card_color(qty):
    """
    Возвращает цвет фона карточки.

    :param qty: количество товара
    :return: HEX-цвет
    """
    return COLOR_HIGHLIGHT if qty <= 3 else COLOR_MAIN_BG


def _add_image(card, product, bg_color):
    """Добавляет изображение товара (или заглушку)."""
    img_frame = tk.Frame(card, bg=bg_color)
    img_frame.pack(side="left", padx=10, pady=10)

    photo = get_product_image(product[6], size=(100, 100))   # вариант 4: фото
    if photo:
        img_label = tk.Label(img_frame, image=photo, bg=bg_color)
        img_label.image = photo
        img_label.pack()
    else:
        tk.Label(img_frame, text="[НЕТ ФОТО]", bg=bg_color,
                 width=10, height=5).pack()


def _add_text_info(card, product, bg_color, qty):
    """Добавляет текстовую информацию о товаре."""
    text_frame = tk.Frame(card, bg=bg_color)
    text_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    # Проверка значений (крайние случаи)
    name = shorten(product[2]) if product[2] else "[Без названия]"
    weight = product[3] if product[3] else "?"
    category = product[1] if product[1] else "[Без категории]"
    composition = product[7] if product[7] else "[Не указан]"
    price = product[4] if product[4] is not None else 0
    price = calculate_price_with_discount(product[0], price, datetime.now())

    # в варианте 4 нет поля «производство», вместо него вес
    _add_label(text_frame, f"{name} | {weight} г",
               bg_color, bold=True, size=FONT_SIZE_HEADER)
    _add_label(text_frame, f"Категория: {category}", bg_color)

    # Количество с индикатором
    indicator = _indicator(qty)
    _add_label(text_frame, f"Количество: {indicator} ({qty})", bg_color)

    _add_label(text_frame, f"Состав: {composition}", bg_color)
    _add_label(text_frame, f"{format_price(price)} руб.",
               bg_color, bold=True, size=FONT_SIZE_HEADER, align="e")


def _add_label(parent, text, bg_color, bold=False,
               size=FONT_SIZE_NORMAL, align="w"):
    """Добавляет метку с текстом."""
    tk.Label(parent, text=text, font=font(size, bold=bold),
             bg=bg_color, anchor=align).pack(fill="x")


def _indicator(qty):
    """
    Индикатор «много/мало» (порог 5).

    :param qty: количество товара
    :return: «много» или «мало»
    """
    return "много" if qty > 5 else "мало"


def format_price(price):
    """Форматирует цену с разделителем тысяч."""
    if price == int(price):
        return f"{price:,.0f}".replace(",", " ")
    return f"{price:,.1f}".replace(",", " ")


def shorten(text, max_len=MAX_NAME_LEN):
    """Обрезает слишком длинное название."""
    if len(text) > max_len:
        return text[:max_len] + "..."
    return text

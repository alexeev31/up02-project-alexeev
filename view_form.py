"""Форма просмотра товара."""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from styles import (
    COLOR_MAIN_BG, COLOR_SECONDARY_BG, COLOR_ACCENT,
    FONT_SIZE_NORMAL, FONT_SIZE_HEADER, FONT_SIZE_TITLE, font
)
from resources import load_image, get_product_image
from discount import calculate_price_with_discount
from error_handler import safe_call, validate_positive_int
from db_products import get_product_sizes
from order_manager import (
    add_order_to_db,
    update_product_quantity,
    get_product_quantity
)


class ViewForm:
    """
    Форма просмотра выбранного товара.

    Открывается при клике на карточку в каталоге.
    """

    def __init__(self, parent, product, on_add_to_order=None):
        """
        Инициализация формы.

        :param parent: родительское окно
        :param product: кортеж с данными товара из БД
        :param on_add_to_order: callback для добавления в заказ
        """
        self.product = product
        self.on_add_to_order = on_add_to_order

        self.window = tk.Toplevel(parent)
        self.window.title(f"Просмотр — {product[2]}")   # вариант 4: название
        self.window.geometry("700x600")
        self.window.configure(bg=COLOR_MAIN_BG)

        self.build_ui()

    def build_ui(self):
        """Строит интерфейс формы."""
        # Шапка — ГОТОВО
        header = tk.Frame(self.window, bg=COLOR_SECONDARY_BG, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="КАРТОЧКА ТОВАРА",
                 font=font(FONT_SIZE_TITLE, bold=True),
                 bg=COLOR_SECONDARY_BG).pack(pady=15)

        # Основная область — ГОТОВО
        main = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        main.pack(fill="both", expand=True, padx=20, pady=20)

        # Изображение — ГОТОВО
        img_frame = tk.Frame(main, bg=COLOR_MAIN_BG)
        img_frame.pack(side="left", padx=10)

        photo = get_product_image(self.product[6], size=(200, 200))   # вариант 4: фото
        if photo:
            img_label = tk.Label(img_frame, image=photo, bg=COLOR_MAIN_BG)
            img_label.image = photo
            img_label.pack()

        # Информация
        info_frame = tk.Frame(main, bg=COLOR_MAIN_BG)
        info_frame.pack(side="left", fill="both", expand=True, padx=20)

        # вариант 4: производства и размеров в БД нет — вместо них вес и количество
        price = safe_call(calculate_price_with_discount,
                          self.product[0], self.product[4], datetime.now())
        if price is None:
            price = self.product[4]
        self._add_field(info_frame, "Вес", f"{self.product[3]} г")
        self._add_field(info_frame, "Наименование", self.product[2])
        self._add_field(info_frame, "Категория", self.product[1])
        self._add_field(info_frame, "Состав", self.product[7])
        self._add_field(info_frame, "Цена", f"{price} руб.")
        self._add_field(info_frame, "Количество", f"{self.product[5]} шт.")

        # Поле ввода количества для заказа (ДЗ)
        qty_row = tk.Frame(info_frame, bg=COLOR_MAIN_BG)
        qty_row.pack(fill="x", pady=3)
        tk.Label(qty_row, text="В заказ, шт.:", font=font(FONT_SIZE_NORMAL, bold=True),
                 width=15, anchor="w", bg=COLOR_MAIN_BG).pack(side="left")
        self.qty_var = tk.StringVar(value="1")
        tk.Entry(qty_row, textvariable=self.qty_var, width=6,
                 font=font(FONT_SIZE_NORMAL)).pack(side="left")

        # === Выбор размера (если есть) ===
        size_frame = tk.Frame(info_frame, bg=COLOR_MAIN_BG)
        size_frame.pack(fill="x", pady=3)
        tk.Label(size_frame, text="Размер:", font=font(FONT_SIZE_NORMAL, bold=True),
                 width=15, anchor="w", bg=COLOR_MAIN_BG).pack(side="left")

        # Получаем размеры из БД (в варианте 4 размеров нет — будет «—»)
        sizes = get_product_sizes(self.product[0])
        if not sizes:
            sizes = ["—"]

        self.size_var = tk.StringVar(value=sizes[0])
        size_combo = ttk.Combobox(size_frame, textvariable=self.size_var,
                                  values=sizes, state="readonly", width=5,
                                  font=font(FONT_SIZE_NORMAL))
        size_combo.pack(side="left")

        # Кнопки
        btn_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        btn_frame.pack(fill="x", pady=10)

        tk.Button(btn_frame, text="Добавить в заказ", command=self.add_to_order,
                  bg=COLOR_ACCENT, fg="white", font=font(FONT_SIZE_NORMAL),
                  padx=15, pady=5).pack(side="left", padx=20)
        tk.Button(btn_frame, text="Назад", command=self.window.destroy,
                  bg=COLOR_ACCENT, fg="white", font=font(FONT_SIZE_NORMAL),
                  padx=15, pady=5).pack(side="right", padx=20)

    def _add_field(self, parent, label, value):
        """Добавляет поле в форму."""
        row = tk.Frame(parent, bg=COLOR_MAIN_BG)
        row.pack(fill="x", pady=3)

        tk.Label(row, text=f"{label}:", font=font(FONT_SIZE_NORMAL, bold=True),
                 width=15, anchor="w", bg=COLOR_MAIN_BG).pack(side="left")
        tk.Label(row, text=str(value), font=font(FONT_SIZE_NORMAL),
                 anchor="w", bg=COLOR_MAIN_BG).pack(side="left")

    def add_to_order(self):
        """Обработчик кнопки «Добавить в заказ»."""
        if not self.product:
            messagebox.showerror("Ошибка", "Товар не выбран")
            return

        # количество из поля ввода (ДЗ пары 19)
        ok, qty = validate_positive_int(self.qty_var.get(), "Количество")
        if not ok:
            messagebox.showwarning("Ошибка ввода", qty)
            return

        try:
            product_id = self.product[0]
            current_qty = get_product_quantity(product_id)

            if current_qty < qty:
                messagebox.showwarning("Товар закончился",
                                       f"Доступно только {current_qty} шт.")
                return

            new_qty = current_qty - qty
            add_order_to_db("Иванов Иван Иванович", product_id, qty)
            update_product_quantity(product_id, new_qty)

            messagebox.showinfo("Успех", f"Товар добавлен в заказ ({qty} шт.)")

            if self.on_add_to_order:
                self.on_add_to_order()

        except Exception as e:
            messagebox.showerror("Ошибка заказа", f"Не удалось добавить товар:\n{e}")

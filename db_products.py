"""Загрузка товаров из БД в объекты класса Product."""
import sqlite3
from config import DB_PATH
from models import Product


def row_to_product(row):
    """Строка таблицы «Товар» -> объект Product.

    Вариант 4: id, категория, название, вес, цена, количество, фото, состав
    """
    return Product(
        product_id=row[0],
        name=row[2],
        category=row[1],
        price=row[4],
        quantity=row[5],
        weight=row[3],
        image=row[6],
        composition=row[7],
    )


def get_all_products():
    """Возвращает список объектов Product из БД."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    return [row_to_product(row) for row in rows]


def get_products_by_category(category):
    """Возвращает список объектов Product по категории."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар WHERE категория = ?", (category,))
    rows = cur.fetchall()
    conn.close()
    return [row_to_product(row) for row in rows]


def get_products_low_stock():
    """Возвращает товары с количеством ≤ 3."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар WHERE количество <= 3")
    rows = cur.fetchall()
    conn.close()
    return [row_to_product(row) for row in rows]


def print_products(products):
    """Выводит информацию о товарах."""
    print(f"\nВсего товаров: {len(products)}\n")
    for p in products:
        print(p.info())
        print("-" * 60)


def print_catalog_with_highlight(products):
    """Выводит каталог с подсветкой для товаров ≤3."""
    print(f"\n{'=' * 70}")
    print(f"КАТАЛОГ ({len(products)} товаров)")
    print("=" * 70)

    if not products:
        print("   (нет товаров)")

    for p in products:
        highlight = "⚠️" if p.is_low_stock() else "  "
        print(f"{highlight} {p.info()}")

    print("=" * 70)


if __name__ == "__main__":
    print("1. Все товары:")
    print_catalog_with_highlight(get_all_products())

    print("\n2. Товары категории «Пицца»:")
    print_catalog_with_highlight(get_products_by_category("Пицца"))

    print("\n3. Товары с низким остатком (≤3):")
    print_catalog_with_highlight(get_products_low_stock())

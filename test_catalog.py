"""Тестирование каталога."""
import os

import database as db
from catalog import format_price, shorten, MAX_NAME_LEN
from resources import RESOURCES_DIR

# индексы полей (вариант 4)
NAME, PRICE, QTY, IMAGE = 2, 4, 5, 6


def test_db_available():
    """
    Проверяет, что БД доступна.
    """
    try:
        products = db.get_all_products()
        return isinstance(products, list)
    except Exception as e:
        print(f"❌ БД недоступна: {e}")
        return False


def test_products_count():
    """
    Проверяет, что товары загружены.
    """
    products = db.get_all_products()
    return len(products) > 0


def test_product_fields():
    """
    Проверяет, что у всех товаров достаточно полей.
    """
    products = db.get_all_products()
    for p in products:
        if len(p) < 8:
            print(f"❌ Товар id={p[0]}: мало полей ({len(p)})")
            return False
    return True


def test_prices_are_numbers():
    """
    Проверяет, что все цены — числа.
    """
    products = db.get_all_products()
    for p in products:
        if not isinstance(p[PRICE], (int, float)):
            print(f"❌ Товар id={p[0]}: цена не число")
            return False
    return True


def test_quantity_not_negative():
    """
    Проверяет, что количество не отрицательное.
    """
    products = db.get_all_products()
    for p in products:
        if p[QTY] < 0:
            print(f"❌ Товар id={p[0]}: отрицательное количество")
            return False
    return True


def test_names_not_empty():
    """Проверяет, что у всех товаров есть название."""
    products = db.get_all_products()
    for p in products:
        if not p[NAME]:   # пустое или None
            print(f"❌ Товар id={p[0]}: пустое название")
            return False
    return True


def test_has_image():
    """ДЗ пары 18: хотя бы у одного товара есть изображение."""
    products = db.get_all_products()
    for p in products:
        if p[IMAGE] and os.path.exists(os.path.join(RESOURCES_DIR, p[IMAGE])):
            return True
    print("❌ Ни у одного товара нет изображения")
    return False


def test_edge_cases():
    """ДЗ пары 12: цена > 1 000 000, длинное название, кириллица."""
    return (format_price(1250000) == "1 250 000"
            and format_price(0) == "0"
            and len(shorten("Очень длинное название " * 5)) <= MAX_NAME_LEN + 3
            and shorten("Тирамису с ягодами") == "Тирамису с ягодами")


def run_all_tests():
    """
    Прогон всех тестов каталога.
    """
    tests = [
        ("БД доступна", test_db_available),
        ("Товары загружены", test_products_count),
        ("У всех товаров нужные поля", test_product_fields),
        ("Все цены — числа", test_prices_are_numbers),
        ("Количество не отрицательное", test_quantity_not_negative),
        ("Названия не пустые", test_names_not_empty),
        ("Хотя бы у одного товара есть фото", test_has_image),
        ("Цена и длинные названия (пара 12)", test_edge_cases),
    ]

    print("=" * 60)
    print("ТЕСТИРОВАНИЕ КАТАЛОГА")
    print("=" * 60)

    passed = 0
    for name, func in tests:
        result = func()
        status = "✅" if result else "❌"
        if result:
            passed += 1
        print(f"{status} {name}")

    print("=" * 60)
    print(f"Пройдено: {passed} / {len(tests)}")


if __name__ == "__main__":
    run_all_tests()

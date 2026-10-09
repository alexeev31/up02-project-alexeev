"""Проверка вывода полей."""
import os

import database as db
from catalog import format_price, shorten, MAX_NAME_LEN
from resources import RESOURCES_DIR

# индексы полей (вариант 4)
PRICE, QTY, IMAGE = 4, 5, 6


def test_fields():
    """Проверяет, что все поля на месте."""
    products = db.get_all_products()
    print(f"Всего товаров: {len(products)}")

    required_count = 8   # вариант 4: id, категория, название, вес, цена, количество, фото, состав
    errors = 0

    for p in products:
        if len(p) < required_count:
            print(f"❌ Товар id={p[0]}: мало полей ({len(p)})")
            errors += 1

    if errors == 0:
        print("✅ Все товары содержат нужные поля")
    else:
        print(f"❌ Найдено ошибок: {errors}")
    return errors == 0


def test_prices():
    """Проверяет, что у всех товаров есть цена."""
    products = db.get_all_products()
    for p in products:
        if p[PRICE] is None:
            print(f"❌ Товар id={p[0]}: нет цены")
            return False
    print("✅ У всех товаров есть цена")
    return True


def test_quantities():
    """Проверяет, что количество не отрицательное."""
    products = db.get_all_products()
    bad = [p[0] for p in products if p[QTY] is None or p[QTY] < 0]
    if bad:
        print(f"❌ Отрицательное или пустое количество у товаров: {bad}")
        return False
    print("✅ У всех товаров количество ≥ 0")
    return True


def test_images():
    """Проверяет, что хотя бы у одного товара есть изображение (и файл существует)."""
    products = db.get_all_products()
    with_image = [p for p in products
                  if p[IMAGE] and os.path.exists(os.path.join(RESOURCES_DIR, p[IMAGE]))]
    if not with_image:
        print("❌ Ни у одного товара нет изображения")
        return False
    print(f"✅ Изображение есть у {len(with_image)} из {len(products)} товаров "
          f"(у остальных — заглушка)")
    return True


def test_edge_cases():
    """ДЗ: цена > 1 000 000, длинное название, кириллица."""
    checks = [
        ("Цена 1 250 000", format_price(1250000), "1 250 000"),
        ("Цена 412.5", format_price(412.5), "412.5"),
        ("Цена 0", format_price(0), "0"),
        ("Название 120 символов обрезается",
         len(shorten("Очень длинное название " * 5)) <= MAX_NAME_LEN + 3, True),
        ("Короткое кириллическое название не меняется",
         shorten("Тирамису с ягодами"), "Тирамису с ягодами"),
    ]
    ok = True
    for name, result, expected in checks:
        passed = result == expected
        ok = ok and passed
        print(f"{'✅' if passed else '❌'} {name}: {result!r}")
    return ok


if __name__ == "__main__":
    results = [test_fields(), test_prices(), test_quantities(),
               test_images(), test_edge_cases()]
    print("=" * 40)
    print(f"Наборов пройдено: {sum(results)} / {len(results)}")

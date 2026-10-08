"""Тестирование алгоритма скидки."""
from datetime import datetime
from discount import calculate_price_with_discount


def run_tests():
    test_cases = [
        # (product_id, price, date, expected, comment)
        (1, 600, datetime(2026, 10, 15), 600, "Заказы есть в сентябре"),
        (2, 800, datetime(2026, 10, 15), 800, "Заказы есть в сентябре"),
        (3, 400, datetime(2026, 10, 15), 400, "Заказы есть"),
        (4, 350, datetime(2026, 10, 15), 262.5, "Заказов нет → скидка"),
        (5, 550, datetime(2026, 10, 15), 412.5, "Заказов нет → скидка"),

        # Новые тесты
        # исправлено: в октябре 2026 заказов в БД нет → скидка есть
        (2, 800, datetime(2026, 11, 15), 600.0, "В октябре заказов нет → скидка"),
        (1, 600, datetime(2026, 11, 15), 450.0, "В октябре заказов нет → скидка"),
        (4, 350, datetime(2026, 9, 1), 262.5, "Август — заказов нет"),
    ]

    print("=" * 70)
    print("РАСШИРЕННОЕ ТЕСТИРОВАНИЕ АЛГОРИТМА СКИДКИ")
    print("=" * 70)

    passed = 0
    for product_id, price, date, expected, comment in test_cases:
        result = calculate_price_with_discount(product_id, price, date)
        status = "✅" if result == expected else "❌"
        if result == expected:
            passed += 1
        print(f"{status} Товар {product_id} на {date.date()}: "
              f"{price} → {result} (ожидалось {expected}) — {comment}")

    print("=" * 70)
    print(f"Пройдено: {passed} / {len(test_cases)}")


def run_extra_tests():
    """ДЗ: свои тесты на разные даты, товары и размер скидки."""
    test_cases = [
        # (id, цена, дата расчёта, скидка %, ожидание, пояснение)
        (6, 300, datetime(2026, 10, 15), 25, 225.0, "Тирамису — нет заказов в сентябре"),
        (1, 600, datetime(2026, 11, 15), 25, 450.0, "Маргарита — в октябре заказов нет"),
        (1, 600, datetime(2026, 10, 1), 25, 600, "Маргарита — расчёт 1-го числа, сентябрь"),
        (3, 400, datetime(2026, 9, 30), 25, 300.0, "Чизбургер — в августе заказов нет"),
        (4, 350, datetime(2026, 10, 15), 10, 315.0, "Цезарь — скидка 10% вместо 25%"),
    ]

    print("\nДОПОЛНИТЕЛЬНЫЕ ТЕСТЫ (ДЗ)")
    print("=" * 60)

    passed = 0
    for product_id, price, date, percent, expected, comment in test_cases:
        result = calculate_price_with_discount(product_id, price, date, percent)
        status = "✅" if result == expected else "❌"
        if result == expected:
            passed += 1
        print(f"{status} {date:%d.%m.%Y} Товар {product_id}: {price} → {result} "
              f"(ожидалось {expected}) — {comment}")

    print("=" * 60)
    print(f"Пройдено: {passed} / {len(test_cases)}")


def check_all_products(date):
    """ДЗ: цены со скидкой для всех товаров моего варианта БД."""
    from db_products import get_all_products

    print(f"\nЦЕНЫ НА {date:%d.%m.%Y} (вариант 4)")
    print("=" * 60)
    for p in get_all_products():
        new_price = p.price_with_discount_auto(date)
        mark = "скидка 25%" if new_price != p.price else "без скидки"
        print(f"{p.name:<12} {p.price:>7} → {new_price:>7}  ({mark})")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()
    run_extra_tests()
    check_all_products(datetime(2026, 10, 15))

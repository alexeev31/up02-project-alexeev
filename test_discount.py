"""Тестирование алгоритма скидки."""
from datetime import datetime
from discount import calculate_price_with_discount


def run_tests():
    """Прогон тестов."""
    date = datetime(2026, 10, 15)

    test_cases = [
        # (id, цена, ожидание, пояснение)
        (1, 600, 600, "Маргарита — есть заказ 15.09"),
        (2, 800, 800, "Филадельфия — есть заказ 20.09"),
        (3, 400, 400, "Чизбургер — есть заказ 25.09"),
        (4, 350, 262.5, "Цезарь — нет заказов → 25% скидка"),
        (5, 550, 412.5, "Карбонара — нет заказов → скидка"),
    ]

    print("=" * 60)
    print("ТЕСТИРОВАНИЕ АЛГОРИТМА СКИДКИ")
    print("=" * 60)

    passed = 0
    for product_id, price, expected, comment in test_cases:
        result = calculate_price_with_discount(product_id, price, date)
        status = "✅" if result == expected else "❌"
        if result == expected:
            passed += 1
        print(f"{status} Товар {product_id}: {price} → {result} "
              f"(ожидалось {expected}) — {comment}")

    print("=" * 60)
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

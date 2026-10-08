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


if __name__ == "__main__":
    run_tests()

"""Тестирование индикатора «много/мало»."""
from catalog import _indicator


def test_indicator():
    """Прогон тестов для индикатора."""
    test_cases = [
        # (qty, expected, comment)
        (10, "много", "10 > 5"),
        (6, "много", "6 > 5 (граница)"),
        (5, "мало", "5 ≤ 5 (граница)"),
        (4, "мало", "4 ≤ 5"),
        (1, "мало", "1 ≤ 5"),
        (0, "мало", "0 ≤ 5"),
        (100, "много", "большое число"),
        # ДЗ
        (1000, "много", "очень большое число"),
        (50, "много", "среднее значение"),
        (5, "мало", "граница (повторно)"),
        (6, "много", "граница (повторно)"),
        (-1, "мало", "отрицательное количество"),
    ]

    print("=" * 60)
    print("ТЕСТИРОВАНИЕ ИНДИКАТОРА")
    print("=" * 60)

    passed = 0
    for qty, expected, comment in test_cases:
        result = _indicator(qty)
        status = "✅" if result == expected else "❌"
        if result == expected:
            passed += 1
        print(f"{status} qty={qty}: {result} (ожидалось {expected}) — {comment}")

    print("=" * 60)
    print(f"Пройдено: {passed} / {len(test_cases)}")


def test_bad_data():
    """ДЗ пары 18: некорректные данные — падает функция или нет."""
    print("\nНЕКОРРЕКТНЫЕ ДАННЫЕ")
    print("=" * 60)
    for qty in [None, "10", 0.5]:
        try:
            result = _indicator(qty)
            print(f"✅ qty={qty!r}: {result}")
        except Exception as e:
            print(f"❌ qty={qty!r}: ошибка {type(e).__name__}")


if __name__ == "__main__":
    test_indicator()
    test_bad_data()

"""Задание 8. Программа 1: расчёт цены со скидкой."""


def discount(price, percent):
    """Цена со скидкой."""
    return price * (1 - percent / 100)


def main():
    try:
        price = float(input("Введите цену: "))
        percent = float(input("Введите скидку (%): "))
    except ValueError:
        print("Ошибка: нужно ввести число.")
        return

    if price < 0 or not 0 <= percent <= 100:
        print("Ошибка: цена не может быть отрицательной, скидка — от 0 до 100%.")
        return

    print(f"Цена со скидкой: {discount(price, percent):.2f} руб.")


if __name__ == "__main__":
    main()

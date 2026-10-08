"""ДЗ. Программа 4: индикатор «много/мало» (часть Задания 2 ДЭ)."""

from task_03_catalog import catalog


def indicator(qty):
    """«много», если больше 5 шт., иначе «мало»."""
    return "много" if qty > 5 else "мало"


def main():
    # сначала «много», потом «мало»; внутри группы — по убыванию количества
    items = sorted(catalog, key=lambda item: (item["qty"] <= 5, -item["qty"]))

    print("Каталог с индикатором:")
    for i, item in enumerate(items, start=1):
        print(f"{i}. {item['name']} — {item['qty']} шт. → {indicator(item['qty'])}")


if __name__ == "__main__":
    main()

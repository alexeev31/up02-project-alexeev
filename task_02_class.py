"""ДЗ. Программа 2: класс Product и расчёт общей стоимости."""


class Product:
    def __init__(self, name, price, qty):
        self.name = name
        self.price = price
        self.qty = qty

    def total(self):
        """Общая стоимость товара."""
        return self.price * self.qty

    def info(self):
        return f"{self.name}: {self.price} × {self.qty} = {self.total()} руб."


def main():
    products = [
        Product("Кроссовки", 8500, 3),
        Product("Ботинки", 15000, 1),
        Product("Туфли", 12000, 5),
    ]
    for product in products:
        print(product.info())


if __name__ == "__main__":
    main()

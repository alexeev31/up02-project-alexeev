"""Модели данных для проекта УП.02."""


class Product:
    """Класс Товар (вариант 4 — доставка еды)."""

    def __init__(self, product_id, name, category, price, quantity,
                 weight=0, image="", composition=""):
        """
        Инициализация товара.

        :param product_id: идентификатор
        :param name: название
        :param category: категория
        :param price: цена
        :param quantity: количество
        :param weight: вес порции, г
        :param image: имя файла фото
        :param composition: состав
        """
        self.id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.quantity = quantity
        self.weight = weight
        self.image = image
        self.composition = composition

    def total(self):
        """Общая стоимость (цена × количество)."""
        return self.price * self.quantity

    def price_with_discount(self, discount_percent):
        """Цена со скидкой."""
        return self.price * (1 - discount_percent / 100)

    def indicator(self):
        """Индикатор «много/мало» (порог 5)."""
        return "много" if self.quantity > 5 else "мало"

    def has_image(self):
        """Есть ли у товара фото."""
        return bool(self.image)

    def info(self):
        """Строка с информацией о товаре."""
        return (
            f"{self.name} ({self.category}): "
            f"{self.price} руб. × {self.quantity} = {self.total()} руб. "
            f"({self.indicator()})"
        )

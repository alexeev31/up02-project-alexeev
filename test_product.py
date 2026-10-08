"""Проверка класса Product."""
from models import Product


# Создаём один товар вручную
p = Product(
    product_id=1,
    name="Маргарита",
    category="Пицца",
    price=600,
    quantity=3
)

print(p.info())
print(f"Со скидкой 25%: {p.price_with_discount(25):.2f} руб.")

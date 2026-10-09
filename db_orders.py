"""Загрузка заказов из БД."""
import sqlite3
from config import DB_PATH
from models import Product, Order


def get_all_orders():
    """Возвращает список объектов Order."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "SELECT Заказ.id, Заказ.дата, Заказ.клиент, Заказ.количество, "
        "Товар.id, Товар.название, Товар.категория, Товар.цена, Товар.количество "
        "FROM Заказ JOIN Товар ON Заказ.товар_id = Товар.id"
    )
    rows = cur.fetchall()
    conn.close()

    orders = []
    for row in rows:
        product = Product(row[4], row[5], row[6], row[7], row[8])
        order = Order(row[0], row[1], row[2], product, row[3])
        orders.append(order)
    return orders


def print_orders(orders):
    """Выводит заказы."""
    print(f"\nВсего заказов: {len(orders)}\n")
    for order in orders:
        print(order.info())


if __name__ == "__main__":
    print_orders(get_all_orders())

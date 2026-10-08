"""Загрузка заказов из БД в объекты класса Order."""
import sqlite3
from config import DB_PATH
from models import Order
from db_products import row_to_product


def get_all_orders():
    """Возвращает список объектов Order (товар подтягивается через JOIN)."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "SELECT Заказ.id, Заказ.дата, Заказ.клиент, Заказ.количество, Товар.* "
        "FROM Заказ JOIN Товар ON Заказ.товар_id = Товар.id "
        "ORDER BY Заказ.id"
    )
    rows = cur.fetchall()
    conn.close()

    orders = []
    for row in rows:
        order_id, date, client, quantity = row[:4]
        product = row_to_product(row[4:])
        orders.append(Order(order_id, date, client, product, quantity))
    return orders


def print_orders(orders):
    """Выводит заказы и общую сумму."""
    print(f"\nВсего заказов: {len(orders)}\n")
    for order in orders:
        print(order.info())
    print("-" * 60)
    print(f"Итого по всем заказам: {sum(o.total() for o in orders)} руб.")


if __name__ == "__main__":
    print_orders(get_all_orders())

"""Модуль расчёта скидки.

Правило (КИМ ДЭ): скидка 25% на товары, по которым нет заказов
в предыдущем календарном месяце относительно даты расчёта.
"""
from datetime import datetime, timedelta
import sqlite3
from config import DB_PATH

DISCOUNT_PERCENT = 25


def get_previous_month_range(date):
    """
    Возвращает (начало, конец) предыдущего месяца.

    :param date: дата расчёта
    :return: (start_date, end_date) в формате YYYY-MM-DD
    """
    first_day = date.replace(day=1)
    last_day_prev = first_day - timedelta(days=1)
    first_day_prev = last_day_prev.replace(day=1)
    return (
        first_day_prev.strftime("%Y-%m-%d"),
        last_day_prev.strftime("%Y-%m-%d")
    )


def has_orders_in_previous_month(product_id, date):
    """
    Есть ли заказы товара в предыдущем месяце?

    :param product_id: id товара
    :param date: дата расчёта
    :return: True / False
    """
    start, end = get_previous_month_range(date)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "SELECT COUNT(*) FROM Заказ "
        "WHERE товар_id = ? AND дата BETWEEN ? AND ?",
        (product_id, start, end)
    )
    count = cur.fetchone()[0]
    conn.close()
    return count > 0


def calculate_price_with_discount(product_id, price, date, percent=DISCOUNT_PERCENT):
    """
    Рассчитывает цену со скидкой.

    :param product_id: id товара
    :param price: базовая цена
    :param date: дата расчёта
    :param percent: размер скидки, % (по умолчанию 25)
    :return: цена со скидкой или без
    """
    if has_orders_in_previous_month(product_id, date):
        return price
    return round(price * (1 - percent / 100), 2)


if __name__ == "__main__":
    today = datetime.now()
    print(f"Дата расчёта: {today:%d.%m.%Y}")
    print(f"Предыдущий месяц: {get_previous_month_range(today)}")

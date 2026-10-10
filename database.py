"""Запросы к БД для оконного приложения.

Возвращает «сырые» строки таблицы Товар (кортежи).
Порядок полей (вариант 4):
    0 id, 1 категория, 2 название, 3 вес, 4 цена, 5 количество, 6 фото, 7 состав
"""
import sqlite3
from config import DB_PATH


def get_all_products():
    """Все товары по порядку id."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    return rows


def get_categories():
    """Список категорий без повторов."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT категория FROM Товар ORDER BY категория")
    categories = [row[0] for row in cur.fetchall()]
    conn.close()
    return categories


def get_user_by_login(login):
    """
    Ищет пользователя по логину.
    :param login: логин
    :return: кортеж (id, фамилия, имя, отчество, логин, роль) или None
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT Пользователь.id, Пользователь.фамилия,
               Пользователь.имя, Пользователь.отчество,
               Пользователь.логин, Роль.название
        FROM Пользователь
        JOIN Роль ON Пользователь.роль_id = Роль.id
        WHERE Пользователь.логин = ?
    """, (login,))
    row = cur.fetchone()
    conn.close()
    return row

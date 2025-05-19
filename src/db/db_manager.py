from datetime import datetime

import psycopg2

from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER


class DBManager:
    """
    Класс для работы с базой данных PostgreSQL для Telegram-бота-магазина.

    Функции:
    - Получение информации о пользователе
    - Создание пользователя
    - Создание заказа и сохранение его содержимого

    Использует psycopg2 и прямые SQL-запросы.
    """

    def __init__(self):
        """
        Устанавливает соединение с базой данных и создаёт курсор.
        """
        self.conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
        )
        self.conn.autocommit = True
        self.cur = self.conn.cursor()

    def get_user(self, telegram_id: int) -> dict | None:
        """
        Получает пользователя по Telegram ID.

        Возвращает:
            dict с ключами id, name, phone, address или None, если не найден.
        """
        self.cur.execute(
            "SELECT id, name, phone, address FROM users WHERE telegram_id = %s",
            (telegram_id,),
        )
        row = self.cur.fetchone()
        return (
            {"id": row[0], "name": row[1], "phone": row[2], "address": row[3]}
            if row
            else None
        )

    def create_user(self, telegram_id: int, name: str, phone: str, address: str) -> int:
        """
        Создаёт нового пользователя.

        Аргументы:
            telegram_id (int): Telegram ID пользователя
            name (str): имя
            phone (str): номер телефона
            address (str): адрес доставки

        Возвращает:
            int — ID нового пользователя в базе
        """
        self.cur.execute(
            """
            INSERT INTO users (telegram_id, name, phone, address)
            VALUES (%s, %s, %s, %s)
            RETURNING id;
            """,
            (telegram_id, name, phone, address),
        )
        return self.cur.fetchone()[0]

    def create_order(self, user_id: int, items: list[dict], status: str = "new") -> int:
        """
        Создаёт заказ и сохраняет его позиции в таблице order_items.

        Аргументы:
            user_id (int): ID пользователя
            items (list[dict]): список товаров (product_name, quantity, price)
            status (str): статус заказа (по умолчанию "new")

        Возвращает:
            int — ID созданного заказа
        """
        self.cur.execute(
            """
            INSERT INTO orders (user_id, status, created_at)
            VALUES (%s, %s, %s)
            RETURNING id;
            """,
            (user_id, status, datetime.now()),
        )
        order_id = self.cur.fetchone()[0]

        for item in items:
            self.cur.execute(
                """
                INSERT INTO order_items (order_id, product_name, quantity, price)
                VALUES (%s, %s, %s, %s);
                """,
                (order_id, item["product_name"], item["quantity"], item["price"]),
            )

        return order_id

    def __del__(self):
        """
        Закрывает соединение и курсор при удалении объекта.
        """
        self.cur.close()
        self.conn.close()

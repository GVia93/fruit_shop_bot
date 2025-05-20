from datetime import datetime

import psycopg2

from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER
from src.models.products import Product


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
        return {"id": row[0], "name": row[1], "phone": row[2], "address": row[3]} if row else None

    def create_or_update_user(self, telegram_id: int, name: str, phone: str, address: str) -> int:
        """
        Добавляет нового пользователя или обновляет его данные по telegram_id.

        Возвращает:
            int: ID пользователя.
        """
        self.cur.execute(
            """
            INSERT INTO users (telegram_id, name, phone, address)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (telegram_id)
            DO UPDATE SET
                name = EXCLUDED.name,
                phone = EXCLUDED.phone,
                address = EXCLUDED.address
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

    def get_orders_by_status(self, status: str = "new") -> list[dict]:
        """
        Возвращает список заказов с заданным статусом.
        Каждый заказ включает: id, имя, телефон, адрес, время, статус.
        """
        self.cur.execute(
            """
            SELECT 
                o.id, o.status, o.created_at,
                u.name, u.phone, u.address
            FROM orders o
            JOIN users u ON o.user_id = u.id
            WHERE o.status = %s
            ORDER BY o.created_at DESC;
        """,
            (status,),
        )

        rows = self.cur.fetchall()
        return [
            {
                "order_id": row[0],
                "status": row[1],
                "created_at": row[2],
                "name": row[3],
                "phone": row[4],
                "address": row[5],
            }
            for row in rows
        ]

    def update_order_status(self, order_id: int, new_status: str):
        """
        Обновляет статус заказа.
        """
        self.cur.execute(
            """
            UPDATE orders SET status = %s WHERE id = %s
        """,
            (new_status, order_id),
        )

    def get_order_items(self, order_id: int) -> list[dict]:
        """
        Возвращает список товаров в заказе.
        """
        self.cur.execute(
            """
            SELECT product_name, quantity, price
            FROM order_items
            WHERE order_id = %s;
        """,
            (order_id,),
        )

        return [{"name": row[0], "qty": row[1], "price": row[2]} for row in self.cur.fetchall()]

    def get_order_stats(self) -> dict:
        """
        Возвращает статистику заказов: общее число, завершённые, отменённые, выручка.
        """
        self.cur.execute("SELECT COUNT(*) FROM orders;")
        total = self.cur.fetchone()[0]

        self.cur.execute("SELECT COUNT(*) FROM orders WHERE status = 'delivered';")
        delivered = self.cur.fetchone()[0]

        self.cur.execute("SELECT COUNT(*) FROM orders WHERE status = 'canceled';")
        canceled = self.cur.fetchone()[0]

        self.cur.execute(
            """
            SELECT COALESCE(SUM(oi.quantity * oi.price), 0)
            FROM order_items oi
            JOIN orders o ON oi.order_id = o.id
            WHERE o.status = 'delivered';
        """
        )
        revenue = self.cur.fetchone()[0]

        return {"total": total, "delivered": delivered, "canceled": canceled, "revenue": revenue}

    def get_product_by_id(self, product_id: int) -> Product | None:
        """
        Возвращает товар по ID из базы данных.
        """
        self.cur.execute("SELECT id, name, price, category FROM products WHERE id = %s", (product_id,))
        row = self.cur.fetchone()
        return Product(*row) if row else None

    def get_products_by_category(self, category: str) -> list[Product]:
        """
        Возвращает список товаров из указанной категории.
        """
        self.cur.execute("SELECT id, name, price, category FROM products WHERE category = %s", (category,))
        return [Product(*row) for row in self.cur.fetchall()]

    def add_product(self, product: Product) -> int:
        """
        Добавляет товар в таблицу products.
        """
        self.cur.execute(
            """
            INSERT INTO products (name, price, category)
            VALUES (%s, %s, %s)
            RETURNING id;
            """,
            (product.name, product.price, product.category),
        )
        return self.cur.fetchone()[0]

    def get_all_products(self) -> list[Product]:
        """
        Возвращает список всех товаров из базы.
        """
        self.cur.execute("SELECT id, name, price, category FROM products ORDER BY id;")
        return [Product(*row) for row in self.cur.fetchall()]

    def delete_product_by_id(self, product_id: int) -> bool:
        """
        Удаляет товар по ID.

        Возвращает:
            True — если товар был успешно удалён,
            False — если товар не найден.
        """
        self.cur.execute("DELETE FROM products WHERE id = %s RETURNING id;", (product_id,))
        return bool(self.cur.fetchone())

    def __del__(self):
        """
        Закрывает соединение и курсор при удалении объекта.
        """
        self.cur.close()
        self.conn.close()

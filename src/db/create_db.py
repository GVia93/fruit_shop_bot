import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER


def create_database_and_tables():
    """
    Создаёт базу данных и таблицы:
    - users
    - orders
    - order_items
    """
    # Подключение к системной базе для создания основной
    conn = psycopg2.connect(
        dbname="postgres",
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    # Проверка существования БД
    cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{DB_NAME}'")
    exists = cur.fetchone()
    if not exists:
        cur.execute(f"CREATE DATABASE {DB_NAME}")
        print(f"База данных '{DB_NAME}' создана.")
    else:
        print(f"База данных '{DB_NAME}' уже существует.")

    cur.close()
    conn.close()

    # Подключение к целевой БД
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    )
    cur = conn.cursor()

    # Создание таблиц
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            telegram_id BIGINT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL
        );
    """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            status TEXT NOT NULL DEFAULT 'new',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS order_items (
            id SERIAL PRIMARY KEY,
            order_id INTEGER REFERENCES orders(id),
            product_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price INTEGER NOT NULL
        );
    """
    )

    conn.commit()
    cur.close()
    conn.close()
    print("Таблицы успешно созданы.")

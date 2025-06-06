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
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()

    # Создание таблиц
    cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                telegram_id BIGINT UNIQUE NOT NULL,
                name TEXT,
                phone TEXT,
                address TEXT
            );
        """)

    cur.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                price INTEGER NOT NULL,
                category TEXT NOT NULL,
                unit TEXT NOT NULL DEFAULT 'kg'
            );
        """)

    cur.execute("""
            CREATE TABLE IF NOT EXISTS cart_items (
                user_telegram_id BIGINT NOT NULL,
                product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
                quantity NUMERIC NOT NULL,
                PRIMARY KEY (user_telegram_id, product_id)
            );
        """)

    cur.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                status TEXT NOT NULL DEFAULT 'new',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

    cur.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                id SERIAL PRIMARY KEY,
                order_id INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
                product_name TEXT NOT NULL,
                quantity NUMERIC NOT NULL,
                price INTEGER NOT NULL
            );
        """)

    conn.commit()
    cur.close()
    conn.close()
    print("Таблицы успешно созданы.")


if __name__ == "__main__":
    create_database_and_tables()

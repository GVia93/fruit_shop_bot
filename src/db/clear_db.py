import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def clear_database():
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    conn.autocommit = True
    cur = conn.cursor()

    try:
        # Очистка в правильном порядке (child → parent)
        cur.execute("DELETE FROM order_items;")
        cur.execute("DELETE FROM orders;")
        cur.execute("DELETE FROM users;")
        cur.execute("DELETE FROM products;")
        print("✅ Все таблицы успешно очищены.")
    except Exception as e:
        print(f"❌ Ошибка при очистке базы: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    clear_database()

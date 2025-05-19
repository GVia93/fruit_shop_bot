import os

from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

# Конфигурация базы данных PostgreSQL
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "fruit_shop")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")

# Telegram Bot Token
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Telegram ID администратора
ADMIN_ID = int(
    os.getenv("ADMIN_ID", "123456789")
)  # обязательно заменить на реальный ID

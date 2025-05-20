import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from src.db.create_db import create_database_and_tables
from src.handlers import admin, cart, catalog, order, start


def init_bot() -> Bot:
    """
    Создаёт экземпляр бота с настройками по умолчанию.
    """
    return Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def main():
    """
    Точка входа: запускает Telegram-бота.
    - Инициализирует БД (если нужно)
    - Регистрирует роутеры
    - Запускает polling
    """
    # Создание базы и таблиц (если не существует)
    create_database_and_tables()

    # Инициализация бота и диспетчера
    bot = init_bot()
    dp = Dispatcher(storage=MemoryStorage())

    # Регистрируем все обработчики
    dp.include_routers(start.router, catalog.router, cart.router, order.router, admin.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

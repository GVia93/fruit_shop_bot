from aiogram import F, Router
from aiogram.types import Message

from src.keyboards.main_menu import main_menu_keyboard

router = Router()


@router.message(F.text == "/start")
async def start_handler(message: Message):
    """
    Обрабатывает команду /start.

    Показывает приветствие и главное меню с кнопками:
    - Категории
    - Корзина
    """
    await message.answer("Добро пожаловать в наш магазин! 🍎\nВыберите действие:", reply_markup=main_menu_keyboard())

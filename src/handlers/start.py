from aiogram import Router, F
from aiogram.types import Message
from src.keyboards.categories import categories_keyboard

router = Router()

@router.message(F.text == "/start")
async def start_handler(message: Message):
    """
    Обрабатывает команду /start.

    Отправляет приветствие и меню категорий.
    """
    await message.answer(
        "Добро пожаловать в наш магазин! 🍎\nВыберите категорию:",
        reply_markup=categories_keyboard()
    )

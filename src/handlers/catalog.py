from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from src.db.db_manager import DBManager
from src.keyboards.categories import categories_keyboard
from src.keyboards.products import products_keyboard

router = Router()
db = DBManager()


@router.callback_query(F.data.startswith("category:"))
async def show_products(callback: CallbackQuery):
    """
    Обрабатывает выбор категории.
    Загружает и показывает товары из базы данных по категории.
    """
    category = callback.data.split(":")[1]
    products = db.get_products_by_category(category)

    if not products:
        await callback.message.answer("В этой категории пока нет товаров.")
        await callback.answer()
        return

    for product in products:
        await callback.message.answer(product.as_text(), reply_markup=products_keyboard(product.id))

    await callback.answer()


@router.message(F.text == "🛍 Категории")
async def show_categories_menu(message: Message):
    """
    Обрабатывает нажатие кнопки 'Категории' и показывает inline-меню категорий.
    """
    await message.answer("Выберите категорию:", reply_markup=categories_keyboard())

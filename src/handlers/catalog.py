from aiogram import Router, F
from aiogram.types import CallbackQuery
from src.keyboards.products import products_keyboard
from src.models.products import products

router = Router()

@router.callback_query(F.data.startswith("category:"))
async def show_products(callback: CallbackQuery):
    """
    Показывает список товаров выбранной категории.

    Фильтрует товары по category из callback_data и отправляет их пользователю.
    """
    category = callback.data.split(":")[1]
    filtered = [p for p in products if p.category == category]

    if not filtered:
        await callback.message.answer("В этой категории пока нет товаров.")
        return

    for product in filtered:
        await callback.message.answer(
            f"<b>{product.name}</b>\nЦена: {product.price}₽",
            reply_markup=products_keyboard(product.id)
        )
    await callback.answer()


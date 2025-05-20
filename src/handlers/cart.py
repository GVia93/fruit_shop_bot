from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.keyboards.cart import cart_keyboard
from src.services.cart import (add_to_cart, clear_cart, get_cart,
                               get_product_by_id)

router = Router()


@router.callback_query(F.data.startswith("cart:add:"))
async def handle_add_to_cart(callback: CallbackQuery, state: FSMContext):
    """
    Добавляет товар в корзину.

    Извлекает product_id из callback_data и сохраняет/обновляет его
    в FSMContext. Показывает уведомление пользователю.

    Формат callback_data: cart:add:<product_id>
    """
    product_id = int(callback.data.split(":")[2])
    await add_to_cart(state, product_id)
    await callback.answer("Добавлено в корзину!")


@router.message(F.text == "🧺 Корзина")
async def show_cart_message(message: Message, state: FSMContext):
    """
    Обрабатывает нажатие кнопки 'Корзина'.
    Показывает текущую корзину пользователя.
    """
    cart = await get_cart(state)

    if not cart:
        await message.answer("Корзина пуста 🧺")
        return

    msg = "<b>🛒 Ваша корзина:</b>\n\n"
    total = 0

    for pid, qty in cart.items():
        product = get_product_by_id(pid)
        if product:
            subtotal = product.price * qty
            total += subtotal
            msg += f"{product.name} x {qty} = {subtotal}₽\n"

    msg += f"\n<b>Итого: {total}₽</b>"

    await message.answer(msg, reply_markup=cart_keyboard())


@router.callback_query(F.data == "cart:clear")
async def handle_clear_cart(callback: CallbackQuery, state: FSMContext):
    """
    Очищает корзину пользователя.

    Удаляет все товары из FSMContext и отправляет сообщение об очистке.
    """
    await clear_cart(state)
    await callback.message.answer("Корзина очищена 🧹")
    await callback.answer()

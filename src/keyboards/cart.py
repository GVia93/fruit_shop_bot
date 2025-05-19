from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def cart_keyboard() -> InlineKeyboardMarkup:
    """
    Кнопка для очистки корзины.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🧹 Очистить", callback_data="cart:clear")],
            [InlineKeyboardButton(text="✅ Оформить заказ", callback_data="order:start")],
        ]
    )

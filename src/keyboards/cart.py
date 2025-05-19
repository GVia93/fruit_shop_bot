from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def cart_keyboard() -> InlineKeyboardMarkup:
    """
    Кнопка для очистки корзины.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🧹 Очистить", callback_data="cart:clear")]
    ])

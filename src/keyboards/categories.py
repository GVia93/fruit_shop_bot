from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def categories_keyboard() -> InlineKeyboardMarkup:
    """
    Клавиатура с кнопками категорий и корзины.
    """
    buttons = [
        [InlineKeyboardButton(text="🍎 Фрукты", callback_data="category:fruits")],
        [InlineKeyboardButton(text="🥦 Овощи", callback_data="category:vegetables")],
        [InlineKeyboardButton(text="🍓 Ягоды", callback_data="category:berries")],
        [InlineKeyboardButton(text="🍄 Грибы", callback_data="category:mushrooms")],
        [InlineKeyboardButton(text="🛒 Корзина", callback_data="cart:view")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

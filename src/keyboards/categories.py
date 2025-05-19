from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def categories_keyboard() -> InlineKeyboardMarkup:
    """
    Клавиатура с кнопками категорий.
    """
    buttons = [
        [InlineKeyboardButton(text="🍎 Фрукты", callback_data="category:fruits")],
        [InlineKeyboardButton(text="🥦 Овощи", callback_data="category:vegetables")],
        [InlineKeyboardButton(text="🍓 Ягоды", callback_data="category:berries")],
        [InlineKeyboardButton(text="🍄 Грибы", callback_data="category:mushrooms")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

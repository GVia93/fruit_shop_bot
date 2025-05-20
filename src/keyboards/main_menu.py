from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    """
    Главное меню пользователя с кнопками:
    - Категории
    - Корзина

    Отображается при запуске бота (/start).
    """
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🛍 Категории"), KeyboardButton(text="🧺 Корзина")]],
        resize_keyboard=True,
        input_field_placeholder="Выберите действие...",
    )

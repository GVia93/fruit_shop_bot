from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def confirm_order_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Подтвердить", callback_data="order:confirm"),
                InlineKeyboardButton(text="✏️ Изменить данные", callback_data="order:edit"),
            ]
        ]
    )

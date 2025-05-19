
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def products_keyboard(product_id: int) -> InlineKeyboardMarkup:
    """
    Кнопка для добавления товара в корзину.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ В корзину", callback_data=f"cart:add:{product_id}")]
    ])

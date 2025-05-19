from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.models.products import Product


def admin_menu_keyboard() -> InlineKeyboardMarkup:
    """
    Клавиатура главного меню администратора:
    - Заказы
    - Статистика
    - Товары
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📦 Заказы", callback_data="admin:orders"),
                InlineKeyboardButton(text="📊 Статистика", callback_data="admin:stats"),
            ],
            [InlineKeyboardButton(text="📋 Товары", callback_data="admin:products")],
        ]
    )


def product_management_keyboard() -> InlineKeyboardMarkup:
    """
    Клавиатура управления товарами:
    - Добавить
    - Удалить
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="➕ Добавить товар", callback_data="admin:product:add"),
                InlineKeyboardButton(text="❌ Удалить товар", callback_data="admin:product:delete"),
            ]
        ]
    )


def admin_order_actions_keyboard(order_id: int) -> InlineKeyboardMarkup:
    """
    Кнопки: Завершить и Отменить заказ.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📦 Завершить", callback_data=f"order:done:{order_id}"),
                InlineKeyboardButton(text="❌ Отменить", callback_data=f"order:cancel:{order_id}"),
            ]
        ]
    )


def delete_product_keyboard(products: list[Product]) -> InlineKeyboardMarkup:
    """
    Генерирует инлайн-кнопки для удаления каждого товара.
    """
    keyboard = [[InlineKeyboardButton(text=f"❌ {p.name} ({p.id})", callback_data=f"delete:{p.id}")] for p in products]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

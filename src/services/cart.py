from aiogram.fsm.context import FSMContext
from src.models.products import Product, products

CART_KEY = "cart"

def get_product_by_id(product_id: int) -> Product | None:
    """
    Возвращает товар по его ID из списка products.
    """
    return next((p for p in products if p.id == product_id), None)


async def add_to_cart(state: FSMContext, product_id: int):
    """
    Добавляет товар в корзину (FSMContext).
    Увеличивает количество, если товар уже есть.
    """
    cart = await state.get_data()
    cart_items = cart.get(CART_KEY, {})

    if product_id in cart_items:
        cart_items[product_id] += 1
    else:
        cart_items[product_id] = 1

    await state.update_data({CART_KEY: cart_items})


async def get_cart(state: FSMContext) -> dict[int, int]:
    """
    Возвращает текущую корзину из FSMContext.
    """
    cart = await state.get_data()
    return cart.get(CART_KEY, {})


async def clear_cart(state: FSMContext):
    """
    Очищает корзину пользователя в FSMContext.
    """
    await state.update_data({CART_KEY: {}})

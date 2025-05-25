from aiogram.fsm.context import FSMContext

from src.db.db_manager import DBManager
from src.models.products import Product

CART_KEY = "cart"


def get_product_by_id(product_id: int) -> Product | None:
    """
    Возвращает товар по его ID из списка products.
    """
    db = DBManager()
    product = db.get_product_by_id(product_id)
    return product


async def add_to_cart(state: FSMContext, product_id: int, quantity: float = 1.0):
    """
    Добавляет товар в корзину (FSMContext).

    Если товар уже есть — увеличивает количество на `quantity`,
    иначе добавляет новый товар с заданным количеством.
    """
    data = await state.get_data()
    cart: dict[int, float] = data.get(CART_KEY, {})
    cart = dict(cart)  # создаём копию

    cart[product_id] = cart.get(product_id, 0) + quantity

    await state.update_data({CART_KEY: cart})

    # отладка
    print("DEBUG cart updated:", cart)


async def get_cart(state: FSMContext) -> dict[int, float]:
    """
    Возвращает текущую корзину из FSMContext.
    """
    data = await state.get_data()
    return data.get(CART_KEY, {})


async def clear_cart(state: FSMContext):
    """
    Очищает корзину пользователя в FSMContext.
    """
    await state.update_data({CART_KEY: {}})

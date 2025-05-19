from aiogram.fsm.state import State, StatesGroup


class OrderForm(StatesGroup):
    """
    Состояния формы оформления заказа.

    Используется для пошагового запроса:
    - имени
    - телефона
    - адреса доставки
    """

    name = State()
    phone = State()
    address = State()

from aiogram.fsm.state import StatesGroup, State

class CartAdd(StatesGroup):
    """
    Состояние для запроса количества товара при добавлении в корзину.
    """
    quantity = State()

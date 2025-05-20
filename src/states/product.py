from aiogram.fsm.state import State, StatesGroup


class AddProduct(StatesGroup):
    """
    Состояния FSM для добавления нового товара администратором.

    Последовательность шагов:
    1. Ввод названия товара
    2. Ввод цены (в рублях)
    3. Ввод категории (например: fruits, vegetables, berries, mushrooms)
    """

    name = State()
    price = State()
    category = State()


class DeleteProduct(StatesGroup):
    """
    Состояния FSM для удаления товара по его ID.

    Последовательность:
    1. Запрос ID товара от администратора
    2. Удаление товара из базы, если найден
    """

    id = State()

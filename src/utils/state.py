from aiogram.fsm.context import FSMContext

ORDER_FIELDS = ["name", "phone", "address", "user_id"]


async def clear_order_form(state: FSMContext):
    """
    Удаляет только поля, относящиеся к форме заказа, не трогая корзину и прочее.
    """
    data = await state.get_data()
    for key in ORDER_FIELDS:
        data.pop(key, None)
    await state.set_data(data)

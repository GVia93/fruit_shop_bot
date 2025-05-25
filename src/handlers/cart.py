from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.db.db_manager import DBManager
from src.keyboards.cart import cart_keyboard
from src.states.cart import CartAdd

router = Router()
db = DBManager()


@router.callback_query(F.data.startswith("cart:add:"))
async def handle_add_to_cart(callback: CallbackQuery, state: FSMContext):
    """
    Запрашивает у пользователя количество (в кг) при добавлении в корзину.
    """
    product_id = int(callback.data.split(":")[2])
    await state.update_data(product_id=product_id)
    await state.set_state(CartAdd.quantity)
    await callback.message.answer("Укажите количество (в кг):")
    await callback.answer()


@router.message(CartAdd.quantity)
async def handle_quantity_input(message: Message, state: FSMContext):
    """
    Обрабатывает ввод количества и сохраняет товар в корзину (в БД).
    """
    try:
        qty = float(message.text.replace(",", "."))
        if qty <= 0:
            raise ValueError
    except ValueError:
        await message.answer("Введите корректное число (например: 1.5)")
        return

    data = await state.get_data()
    product_id = data.get("product_id")
    telegram_id = message.from_user.id

    db.add_to_cart(telegram_id, product_id, qty)
    await message.answer("✅ Добавлено в корзину!")
    await state.clear()


@router.message(F.text == "🧺 Корзина")
async def show_cart_message(message: Message, state: FSMContext):
    """
    Показывает содержимое корзины пользователя (из БД).
    """
    telegram_id = message.from_user.id
    cart = db.get_cart(telegram_id)

    if not cart:
        await message.answer("Корзина пуста 🧺")
        return

    msg = "<b>🛒 Ваша корзина:</b>\n\n"
    total = 0

    for pid, qty in cart.items():
        product = db.get_product_by_id(pid)
        if product:
            subtotal = round(product.price * qty, 2)
            total += subtotal
            msg += f"{product.name} x {round(qty, 2)} кг = {subtotal}₽\n"

    msg += f"\n<b>Итого: {round(total, 2)}₽</b>"

    await message.answer(msg, reply_markup=cart_keyboard())


@router.callback_query(F.data == "cart:clear")
async def handle_clear_cart(callback: CallbackQuery, state: FSMContext):
    """
    Очищает корзину пользователя в БД.
    """
    telegram_id = callback.from_user.id
    db.clear_cart(telegram_id)
    await callback.message.answer("Корзина очищена 🧹")
    await callback.answer()

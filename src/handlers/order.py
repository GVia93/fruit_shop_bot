from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config import ADMIN_ID
from src.db.db_manager import DBManager
from src.keyboards.order import confirm_order_keyboard
from src.services.cart import clear_cart, get_cart
from src.states.order import OrderForm
from src.utils.cart_preview import get_cart_preview_text
from src.utils.state import clear_order_form

router = Router()
db = DBManager()


@router.callback_query(F.data == "order:start")
async def start_order(callback: CallbackQuery, state: FSMContext):
    """
    Обрабатывает начало оформления заказа.

    Если пользователь уже есть в БД — сохраняет его данные в состояние
    и предлагает подтвердить заказ.

    Если пользователь новый — запускает FSM для ввода имени.
    """
    telegram_id = callback.from_user.id
    user = db.get_user(telegram_id)
    cart = await get_cart(state)
    cart_text, total = await get_cart_preview_text(cart)

    if user:
        # Сохраняем данные в FSMContext
        await state.update_data(
            user_id=user["id"],
            name=user["name"],
            phone=user["phone"],
            address=user["address"],
        )

        await callback.message.answer(
            f"✅ Используем ваши сохранённые данные:\n\n"
            f"👤 {user['name']}\n"
            f"📱 {user['phone']}\n"     # f"📍 {user['address']}\n\n"
            f"<b>🛒 Ваша корзина:</b>\n{cart_text}\n\n"
            f"<b>💰 Итого: {total}₽</b>\n\n"
            "Проверьте заказ перед отправкой:",
            reply_markup=confirm_order_keyboard(),
        )
    else:
        await callback.message.answer("Введите ваше имя:")
        await state.set_state(OrderForm.name)

    await callback.answer()


@router.callback_query(F.data == "order:confirm")
async def confirm_order(callback: CallbackQuery, state: FSMContext):
    """
    Подтверждение заказа — запускает сохранение в БД.
    """
    data = await state.get_data()
    if not data.get("user_id"):
        user_id = db.create_or_update_user(
            telegram_id=callback.from_user.id,
            name=data["name"],
            phone=data["phone"],
            address=""
        )
        data["user_id"] = user_id
    await process_order(callback.message, state, data)
    await callback.answer()


@router.callback_query(F.data == "order:edit")
async def edit_order(callback: CallbackQuery, state: FSMContext):
    """
    Перезапускает ввод данных, не очищая корзину.
    """
    await clear_order_form(state)
    await callback.message.answer("Введите ваше имя:")
    await state.set_state(OrderForm.name)
    await callback.answer()


@router.message(OrderForm.name)
async def get_name(message: Message, state: FSMContext):
    """
    Получает имя пользователя и переходит к следующему шагу — телефону.
    """
    await state.update_data(name=message.text)
    await message.answer("Введите номер телефона:")
    await state.set_state(OrderForm.phone)


@router.message(OrderForm.phone)
async def get_phone(message: Message, state: FSMContext):
    """
    Получает телефон пользователя и переходит к следующему шагу — адресу.
    """
    await state.update_data(phone=message.text)
    data = await state.get_data()

    await message.answer(
        f"👤 {data['name']}\n"
        f"📱 {data['phone']}\n\n"
        "Проверьте заказ перед отправкой:",
        reply_markup=confirm_order_keyboard()
    )
    # await message.answer("Введите адрес доставки:")
    # await state.set_state(OrderForm.address)


# @router.message(OrderForm.address)
# async def get_address(message: Message, state: FSMContext):
#     """
#     Получает адрес, сохраняет пользователя в БД и завершает оформление заказа.
#     """
#     await state.update_data(address=message.text)
#     data = await state.get_data()
#
#     user_id = db.create_or_update_user(
#         telegram_id=message.from_user.id, name=data["name"], phone=data["phone"], address=data["address"]
#     )
#
#     data["user_id"] = user_id
#
#     await message.answer(
#         f"✅ Данные обновлены:\n\n"
#         f"👤 {data['name']}\n"
#         f"📱 {data['phone']}\n"
#         f"📍 {data['address']}\n\n"
#         f"Проверьте заказ перед отправкой:",
#         reply_markup=confirm_order_keyboard(),
#     )


async def process_order(message_or_callback, state: FSMContext, data: dict):
    """
    Обрабатывает заказ:
    - Получает корзину из состояния
    - Создаёт заказ в БД
    - Отправляет администратору уведомление
    - Очищает FSM и корзину
    """
    cart = await get_cart(state)
    if not cart:
        await message_or_callback.answer("Корзина пуста 🧺")
        return

    items = []
    total = 0

    for pid, qty in cart.items():
        product = db.get_product_by_id(pid)
        if not product:
            continue
        subtotal = product.price * qty
        total += subtotal
        items.append({"product_name": product.name, "quantity": qty, "price": product.price})

    # Убедимся, что user_id есть
    user_id = data.get("user_id")
    if not user_id:
        await message_or_callback.answer("Ошибка: пользователь не найден.")
        return

    # Создание заказа
    order_id = db.create_order(user_id, items)

    # Уведомление администратору
    item_lines = "\n".join(f"{i['product_name']} x{i['quantity']} = {i['quantity'] * i['price']}₽" for i in items)
    text = (
        f"📦 <b>Новый заказ #{order_id}</b>\n\n"
        f"👤 {data.get('name', 'из базы')}\n"
        f"📱 {data.get('phone', '-')}\n"
        # f"📍 {data.get('address', '-')}\n\n"
        f"{item_lines}\n\n"
        f"💰 <b>Итого: {total}₽</b>"
    )

    await message_or_callback.bot.send_message(ADMIN_ID, text)
    await message_or_callback.answer("✅ Ваш заказ успешно оформлен!")
    await clear_cart(state)
    await state.clear()

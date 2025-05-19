from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config import ADMIN_ID
from src.db.db_manager import DBManager
from src.keyboards.admin_panel import (admin_menu_keyboard,
                                       admin_order_actions_keyboard,
                                       delete_product_keyboard,
                                       product_management_keyboard)
from src.models.products import Product
from src.states.product import AddProduct

router = Router()
db = DBManager()


@router.message(F.text == "/admin")
async def admin_menu(message: Message):
    """
    Показывает админ-панель с кнопками: Заказы, Статистика.
    """
    if message.from_user.id != ADMIN_ID:
        await message.answer("У вас нет доступа.")
        return

    await message.answer("Выберите действие:", reply_markup=admin_menu_keyboard())


@router.callback_query(F.data == "admin:orders")
async def show_new_orders(callback: CallbackQuery):
    """
    Показывает список новых заказов.
    """
    orders = db.get_orders_by_status("new")
    if not orders:
        await callback.message.answer("Нет новых заказов.")
        await callback.answer()
        return

    for order in orders:
        items = db.get_order_items(order["order_id"])
        items_text = "\n".join(f"🍎 {item['name']} x{item['qty']} = {item['qty'] * item['price']}₽" for item in items)

        text = (
            f"📦 <b>Заказ #{order['order_id']}</b>\n"
            f"👤 {order['name']}\n"
            f"📱 {order['phone']}\n"
            f"📍 {order['address']}\n"
            f"🕒 {order['created_at'].strftime('%Y-%m-%d %H:%M')}\n"
            f"📝 Статус: {order['status']}\n\n"
            f"<b>Состав:</b>\n{items_text}"
        )
        await callback.message.answer(text, reply_markup=admin_order_actions_keyboard(order["order_id"]))

    await callback.answer()


@router.callback_query(F.data.startswith("order:cancel:"))
async def cancel_order(callback: CallbackQuery):
    """
    Отменяет заказ (обновляет статус на 'canceled').
    """
    order_id = int(callback.data.split(":")[2])
    db.update_order_status(order_id, "canceled")
    await callback.message.edit_reply_markup()
    await callback.message.answer(f"❌ Заказ #{order_id} отменён.")


@router.callback_query(F.data.startswith("order:done:"))
async def finish_order(callback: CallbackQuery):
    """
    Обновляет статус заказа на 'delivered'.
    Используется для отметки заказа как завершённого.
    """
    order_id = int(callback.data.split(":")[2])
    db.update_order_status(order_id, "delivered")
    await callback.message.edit_reply_markup()
    await callback.message.answer(f"📦 Заказ #{order_id} завершён.")


@router.callback_query(F.data == "admin:stats")
async def show_stats(callback: CallbackQuery):
    """
    Показывает статистику заказов администратору.
    """
    stats = db.get_order_stats()

    text = (
        "<b>📊 Статистика заказов:</b>\n\n"
        f"📦 Всего заказов: {stats['total']}\n"
        f"✅ Завершено: {stats['delivered']}\n"
        f"❌ Отменено: {stats['canceled']}\n"
        f"💰 Выручка: {stats['revenue']} ₽"
    )
    await callback.message.answer(text)
    await callback.answer()


@router.callback_query(F.data == "admin:products")
async def show_product_menu(callback: CallbackQuery):
    """
    Показывает кнопки управления товарами: добавить / удалить.
    """
    await callback.message.answer("Управление товарами:", reply_markup=product_management_keyboard())
    await callback.answer()


@router.callback_query(F.data == "admin:product:add")
async def start_add_product(callback: CallbackQuery, state: FSMContext):
    """
    Старт FSM добавления нового товара.
    """
    await callback.message.answer("Введите название товара:")
    await state.set_state(AddProduct.name)
    await callback.answer()


@router.message(AddProduct.name)
async def get_product_name(message: Message, state: FSMContext):
    """
    Сохраняет введённое имя товара и переходит к шагу ввода цены.
    """
    await state.update_data(name=message.text)
    await message.answer("Введите цену товара в рублях (только число):")
    await state.set_state(AddProduct.price)


@router.message(AddProduct.price)
async def get_product_price(message: Message, state: FSMContext):
    """
    Проверяет корректность введённой цены.
    Сохраняет цену и переходит к выбору категории.
    """
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите только число.")
        return
    await state.update_data(price=int(message.text))
    await message.answer("Введите категорию товара (фрукты, овощи, ягоды, грибы):")
    await state.set_state(AddProduct.category)


@router.message(AddProduct.category)
async def get_product_category(message: Message, state: FSMContext):
    """
    Сохраняет категорию, формирует объект Product,
    добавляет его в базу данных и завершает FSM.
    """
    CATEGORY_MAP = {"фрукты": "fruits", "овощи": "vegetables", "ягоды": "berries", "грибы": "mushrooms"}

    user_input = message.text.strip().lower()
    category = CATEGORY_MAP.get(user_input)

    if not category:
        await message.answer("Неверная категория. Пожалуйста, выберите из: фрукты, овощи, ягоды, грибы.")
        return

    await state.update_data(category=category)
    data = await state.get_data()

    product = Product(id=0, name=data["name"], price=data["price"], category=data["category"])

    db.add_product(product)
    await message.answer(f"✅ Товар <b>{product.name}</b> добавлен в базу данных.")
    await state.clear()


@router.callback_query(F.data == "admin:product:delete")
async def choose_product_to_delete(callback: CallbackQuery):
    """
    Показывает список товаров с кнопками удаления.
    """
    products = db.get_all_products()

    if not products:
        await callback.message.answer("❗ В базе пока нет товаров.")
        await callback.answer()
        return

    await callback.message.answer("Выберите товар для удаления:", reply_markup=delete_product_keyboard(products))
    await callback.answer()


@router.callback_query(F.data.startswith("delete:"))
async def delete_selected_product(callback: CallbackQuery):
    """
    Удаляет выбранный товар по ID из базы данных.
    """
    product_id = int(callback.data.split(":")[1])
    success = db.delete_product_by_id(product_id)

    if success:
        await callback.message.edit_text(f"✅ Товар с ID {product_id} удалён.")
    else:
        await callback.message.answer(f"❌ Товар с ID {product_id} не найден.")
    await callback.answer()

from src.db.db_manager import DBManager

db = DBManager()


async def get_cart_preview_text(telegram_id: int) -> tuple[str, float]:
    """
    Получает корзину пользователя из БД,
    формирует текст для предпросмотра и возвращает итоговую сумму.
    """
    cart = db.get_cart(telegram_id)
    if not cart:
        return "Корзина пуста 🧺", 0.0

    lines = []
    total = 0.0

    for pid, qty in cart.items():
        product = db.get_product_by_id(pid)
        if not product:
            continue
        subtotal = round(product.price * qty, 2)
        total += subtotal
        lines.append(f"{product.name} x{round(qty, 2)} = {subtotal}₽")

    text = "\n".join(lines)
    return text, round(total, 2)

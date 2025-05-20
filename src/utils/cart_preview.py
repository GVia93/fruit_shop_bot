from src.db.db_manager import DBManager

db = DBManager()


async def get_cart_preview_text(cart: dict[int, int]) -> tuple[str, int]:
    """
    Формирует текст для предпросмотра корзины и возвращает его с итоговой суммой.
    """
    lines = []
    total = 0

    for pid, qty in cart.items():
        product = db.get_product_by_id(pid)
        if not product:
            continue
        subtotal = product.price * qty
        total += subtotal
        lines.append(f"{product.name} x{qty} = {subtotal}₽")

    text = "\n".join(lines)
    return text, total

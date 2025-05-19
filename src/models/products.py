from dataclasses import dataclass


@dataclass
class Product:
    """
    Модель товара.
    """

    id: int
    name: str
    price: int  # в рублях
    category: str

    def as_text(self) -> str:
        """
        Возвращает строку для вывода в Telegram.
        """
        return f"<b>{self.name}</b>\nЦена: {self.price}₽"

    def as_cart_line(self, qty: int) -> str:
        """
        Строка позиции в корзине.
        """
        total = self.price * qty
        return f"{self.name} x{qty} = {total}₽"

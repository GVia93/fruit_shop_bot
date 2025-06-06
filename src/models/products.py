from dataclasses import dataclass


@dataclass
class Product:
    """
    Модель товара.
    """

    id: int
    name: str
    price: int
    category: str
    unit: str

    def as_text(self) -> str:
        """
        Возвращает строку для вывода в Telegram.
        """
        return f"<b>{self.name}</b>\nЦена: {self.price}₽ / {self.unit}"

    def as_cart_line(self, qty: float) -> str:
        """
        Строка позиции в корзине с учётом единицы измерения.
        """
        total = self.price * qty
        return f"{self.name} x{round(qty, 2)} {self.unit} = {round(total, 2)}₽"

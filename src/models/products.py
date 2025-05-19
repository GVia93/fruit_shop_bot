from typing import NamedTuple


class Product(NamedTuple):
    """
    Модель товара: id, название, цена, категория.
    """

    id: int
    name: str
    price: int  # в рублях
    category: str


# Мок-данные для тестирования каталога
products = [
    Product(1, "Яблоко", 50, "fruits"),
    Product(2, "Банан", 60, "fruits"),
    Product(3, "Морковь", 30, "vegetables"),
    Product(4, "Огурец", 40, "vegetables"),
    Product(5, "Клубника", 120, "berries"),
    Product(6, "Черника", 150, "berries"),
    Product(7, "Белый гриб", 200, "mushrooms"),
    Product(8, "Шампиньоны", 100, "mushrooms"),
]

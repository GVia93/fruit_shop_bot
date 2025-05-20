# 🛒 Fruit Shop Bot

Telegram-бот-магазин для продажи фруктов, овощей, ягод и грибов.  
Поддерживает корзину, оформление заказа, админ-панель, статистику и управление товарами.

---

## 🚀 Возможности

### 🧍 Пользователь:
- Просмотр товаров по категориям: 🍎 фрукты, 🥦 овощи, 🍓 ягоды, 🍄 грибы
- Добавление товаров в корзину
- Просмотр и очистка корзины
- Оформление заказа с подтверждением данных
- Повторное использование сохранённых данных (профиль)

### 👨‍💼 Администратор:
- Просмотр новых заказов
- Отмена и завершение заказов
- Просмотр статистики по заказам
- Добавление и удаление товаров
- Админ-панель с кнопками управления

---

## 🛠 Установка

### 📦 Требования
- Python 3.11+
- PostgreSQL
- Poetry (рекомендуется)

### ⚙ Установка зависимостей

```bash
poetry install
```

---

## ⚙ Настройка окружения

Создайте файл `.env` в корне проекта:

```env
BOT_TOKEN=your_telegram_bot_token
ADMIN_ID=123456789

DB_HOST=localhost
DB_PORT=5432
DB_NAME=fruitshop
DB_USER=postgres
DB_PASSWORD=your_password
```

---

## 📂 Структура проекта

```text
├── main.py                  # Точка входа
├── config.py                # Загрузка переменных окружения
├── pyproject.toml           # Poetry зависимости
├── README.md
└──  src/
    ├── db/
    │   ├── create_db.py             # Создание таблиц в PostgreSQL
    │   └── db_manager.py        # Работа с базой данных
    │
    ├── handlers/                # Хендлеры aiogram
    │   ├── admin.py
    │   ├── cart.py
    │   ├── catalog.py
    │   ├── order.py
    │   └── start.py
    │
    ├── keyboards/               # Клавиатуры Telegram  
    │   ├── admin_panel.py
    │   ├── cart.py
    │   ├── categories.py
    │   ├── main_menu.py
    │   └── order.py
    │
    ├── models/                  # Модели и структуры данных
    │   └── product.py
    │
    ├── services/                # Бизнес-логика
    │   ├── cart.py
    │   ├── cart_preview.py
    │   └── order.py
    │
    └──states/                  # FSM-состояния
        └── state.py

```

---

## 🧪 Запуск

```bash
# 1. Создание базы данных и таблиц
python create_db.py

# 2. Запуск бота
python main.py
```

---

## 📊 Статусы заказа

| Статус     | Описание           |
|------------|--------------------|
| `new`      | Новый заказ        |
| `delivered`| Завершён           |
| `canceled` | Отменён администратором |

---

## 🧩 Зависимости

- [aiogram v3](https://docs.aiogram.dev/)
- [psycopg2](https://www.psycopg.org/)
- [python-dotenv](https://github.com/theskumar/python-dotenv)

---

## 📌 Автор

Разработка: **[gvia]**  
Контакт: gritcaev.vv@gmail.com

---

## 📜 Лицензия

MIT License

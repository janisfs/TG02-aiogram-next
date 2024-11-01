from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

main = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Тестовая кнопка 1")],
        [KeyboardButton(text="Тестовая кнопка 2"), KeyboardButton(text="Тестовая кнопка 3")]
    ],
    resize_keyboard=True
)

inline_keyboard_test = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Каталог", callback_data="catalog")],
    [InlineKeyboardButton(text="Новости", callback_data="news")],
    [InlineKeyboardButton(text="Профиль", callback_data="profile")],
    [InlineKeyboardButton(text="Цитата", callback_data="quote")]
   ])

test = ["Кнопка 1", "Кнопка 2", "Кнопка 3", "Кнопка 4"]


# message_keyboard - это строка, которая добавляет inline-клавиатуру в сообщение. После клика на кнопку, появляется добавочное меню.
async def message_keyboard():
    keyboard = InlineKeyboardBuilder()
    for key in test:
        keyboard.add(InlineKeyboardButton(text=key, url='https://www.youtube.com/@janisfs'))
    return keyboard.adjust(2).as_markup(resize_keyboard=True)


# test_keyboard - это строка, которая добавляет inline-клавиатуру в сообщение.
async def test_keyboard():
    keyboard = ReplyKeyboardBuilder() # resize_keyboard=True - адаптирует размер клавиатуры
    for key in test:
        keyboard.add(KeyboardButton(text=key))
    return keyboard.adjust(2).as_markup(resize_keyboard=True)




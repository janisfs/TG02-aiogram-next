from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

main = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Тестовая кнопка 1")],
        [KeyboardButton(text="Тестовая кнопка 2"), KeyboardButton(text="Тестовая кнопка 3")]
    ],
    resize_keyboard=True
)

inline_keyboard_test = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="My YouTube channel",
                          url = "https://www.youtube.com/@janisfs")],
   ])

test = ["Кнопка 1", "Кнопка 2", "Кнопка 3", "Кнопка 4"]

async def test_keyboard():
    keyboard = ReplyKeyboardBuilder(resize_keyboard=True) # resize_keyboard=True - адаптирует размер клавиатуры
    for key in test:
        keyboard.add(KeyboardButton(text=key))
    return keyboard.adjust(2).as_markup()




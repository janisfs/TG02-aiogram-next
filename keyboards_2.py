from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


inline_keyboard_greetings = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Привет", callback_data="hello")],
    [InlineKeyboardButton(text="До свидания", callback_data="bye")]
   ])


inline_keyboard_links = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Новости", callback_data="news")],
    [InlineKeyboardButton(text="Музыка", callback_data="music")],
    [InlineKeyboardButton(text="Видео", callback_data="video")]
   ])

# Новая клавиатура с кнопками "Опция 1" и "Опция 2"
options_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Опция 1", callback_data="option_1")],
    [InlineKeyboardButton(text="Опция 2", callback_data="option_2")]
])
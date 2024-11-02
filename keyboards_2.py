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
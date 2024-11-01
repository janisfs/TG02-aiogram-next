from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

inline_keyboard_greetings = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Привет", callback_data="hello")],
    [InlineKeyboardButton(text="До свидания", callback_data="bye")]
   ])

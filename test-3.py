import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile, CallbackQuery
from config import TOKEN
import sqlite3
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
import logging
from aiogram.fsm.state import State, StatesGroup
from aiogram import types
from keyboards_2 import inline_keyboard_greetings
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

import keyboards_2 as kb


bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

logging.basicConfig(level=logging.INFO)

class Form(StatesGroup):
    name = State()


def init_db():
    conn = sqlite3.connect('person_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS person_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT)
            ''')

    conn.commit()
    conn.close()

init_db()

@dp.message(CommandStart())
async def start_menu(message: Message, state: FSMContext):
    await message.answer("Привет! Как твое имя:")
    await state.set_state(Form.name)


@dp.message(Command("help"))
async def help(message: Message):
    await message.answer("Доступные команды:\n"
                         "/start - начать диалог\n"
                         "/help - вызов всех команд, которые может выполнять бот\n"
                         "/links - показать ссылки на новости, музыку и видео"
                         )


@dp.message(Command("links"))
async def links(message: Message, state: FSMContext):
    await message.answer("Выберите ссылку:", reply_markup=kb.inline_keyboard_links)
    # await state.set_state(Form.name) - для случаев привязки к пользователям


@dp.callback_query(F.data == "news")
async def catalog(callback: CallbackQuery):
    await callback.answer("Новости подгружаются...", show_alert=True)
    await callback.message.answer("https://ria.ru/")


@dp.callback_query(F.data == "music")
async def catalog(callback: CallbackQuery):
    await callback.answer("Музыка подгружается...", show_alert=True)
    await callback.message.answer("https://music.yandex.ru/home")


@dp.callback_query(F.data == "video")
async def catalog(callback: CallbackQuery):
    await callback.answer("Видео подгружается...", show_alert=True)
    await callback.message.answer("https://www.youtube.com/")


@dp.message(Form.name)
async def name(message: Message, state: FSMContext):
    print("Получено имя:", message.text)
    await state.update_data(name=message.text)
    user_data = await state.get_data()
    print("Данные:", user_data)

    # Сохранение данных в базе данных
    conn = sqlite3.connect('person_data.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO person_data (name) VALUES (?)''',
                (user_data['name'],))
    conn.commit()
    conn.close()
    print("Данные сохранены!")

    await message.answer("Спасибо!\n Данные сохранены!", reply_markup=inline_keyboard_greetings)


@dp.callback_query()
async def menu_handler(callback_query: types.CallbackQuery, state: FSMContext):
    # Загружаем данные о пользователе из состояния
    user_data = await state.get_data()
    user_name = user_data.get("name")


    # Формируем ответ на основе нажатой кнопки
    if callback_query.data == "hello":
        await callback_query.message.answer(f"Привет, {user_name}!")
    elif callback_query.data == "bye":
        await callback_query.message.answer(f"До свидания, {user_name}!")



async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
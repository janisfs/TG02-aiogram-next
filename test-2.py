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

import keyboards as kb


bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

logging.basicConfig(level=logging.INFO)

class Form(StatesGroup):
    name = State()
    age = State()
    grade = State()


def init_db():
    conn = sqlite3.connect('school_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            grade TEXT)
            ''')

    conn.commit()
    conn.close()

init_db()

@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    # reply_markup=kb.main - это строка, которая добавляет клавиатуру в сообщение.
    # reply_markup=kb.inline_keyboard_test - это строка, которая добавляет inline-клавиатуру в сообщение.
    # reply_markup=await kb.test_keyboard()) - это строка, которая добавляет inline-клавиатуру в сообщение.
    # kb.main - это строка, которая добавляет клавиатуру в сообщение.
    await message.answer("Привет! Введи свое имя и фамилию:", reply_markup=kb.inline_keyboard_test)
    await state.set_state(Form.name)


@dp.callback_query(F.data == "catalog")
async def catalog(callback: CallbackQuery):
    await callback.message.answer("Вы нажали на кнопку 'Каталог'")


@dp.callback_query(F.data == "news")
async def catalog(callback: CallbackQuery):
    await callback.answer("Новости подгружаются...", show_alert=True)
    await callback.message.answer("Вы нажали на кнопку 'Новости'")

@dp.callback_query(F.data == "quote")
async def catalog(callback: CallbackQuery):
    await callback.answer("Свежие цитаты подгружаются...", show_alert=True)
    await callback.message.edit_text("Вы нажали на кнопку 'Цитаты'", reply_markup=await kb.message_keyboard())


@dp.message(F.text == "Тестовая кнопка 1")
async def test_button_1(message: Message):
    await message.answer("Вы нажали на кнопку 1")


@dp.message(Form.name)
async def name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введи свой возраст:")
    await state.set_state(Form.age)


@dp.message(Form.age)
async def age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    age = int(message.text)
    if age < 18:
        grade_text = "класс"
    else:
        grade_text = "курс"
    await message.answer(f"Введи свой {grade_text}:")
    await state.set_state(Form.grade)


@dp.message(Form.grade)
async def grade(message: Message, state: FSMContext):
    await state.update_data(grade=message.text)
    user_data = await state.get_data()

    # Сохранение данных в базе данных
    conn = sqlite3.connect('school_data.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO students (name, age, grade) VALUES (?, ?, ?)''',
                (user_data['name'], user_data['age'], user_data['grade']))
    conn.commit()
    conn.close()

    await message.answer("Спасибо за информацию!\n Данные сохранены!")
    await state.clear()



async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
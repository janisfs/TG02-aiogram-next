import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from config import TOKEN, api_key
from googletrans import Translator
import sqlite3
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import aiohttp
import logging


translator = Translator()
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

logging.basicConfig(level=logging.INFO)

class Form(StatesGroup):
    name = State()
    age = State()
    city = State()

def init_db():
    conn = sqlite3.connect('users_data.db')
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        city TEXT NOT NULL)
    ''')
    conn.commit()
    conn.close()

init_db()

# Обработчик команды /start
@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer("Привет! Я бот. Как тебя зовут?")
    await state.set_state(Form.name)

# Обработчик ввода имени
@dp.message(Form.name)
async def name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите ваш возраст:")
    await state.set_state(Form.age)

# Обработчик ввода возраста
@dp.message(Form.age)
async def age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("Введите ваш город:")
    await state.set_state(Form.city)

# Обработчик ввода города
@dp.message(Form.city)
async def city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    user_data = await state.get_data()

    # Сохранение данных в базе данных
    conn = sqlite3.connect('users_data.db')
    cur = conn.cursor()
    cur.execute('''INSERT INTO users (name, age, city) VALUES (?, ?, ?)''',
                (user_data['name'], user_data['age'], user_data['city']))
    conn.commit()
    conn.close()

    # Получение данных о погоде
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://api.openweathermap.org/data/2.5/weather?q={user_data['city']}"
                                   f"&appid={api_key}&units=metric&lang=ru") as response:
                if response.status == 200:
                    weather_data = await response.json()
                    main = weather_data.get('main')
                    weather = weather_data.get('weather', [{}])[0]

                    if main and weather:
                        temperature = main.get('temp')
                        humidity = main.get('humidity')
                        description = weather.get('description', 'нет описания')

                        weather_report = (f"Погода в {user_data['city']}:\n"
                                          f"Температура: {temperature}°C\n"
                                          f"Влажность: {humidity}%\n"
                                          f"Описание: {description}")
                        await message.answer(weather_report)
                    else:
                        await message.answer("Не удалось получить полные данные о погоде.")
                else:
                    await message.answer(f"Не удалось получить данные о погоде. Код ошибки: {response.status}")
    except Exception as e:
        await message.answer("Произошла ошибка при получении данных о погоде.")
        logging.error(f"Ошибка при запросе погоды: {e}")

    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

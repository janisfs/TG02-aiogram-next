import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from config import TOKEN
import random
import requests

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(F.photo)
async def react_photo(message: Message):
    list = ['Ого, какая фотка!', 'Не понятно, что это может быть!', 'Я не знаю, что это такое!', 'Не отправляйте мне такое больше!', 'Круто!', 'Это очень красивое фото!']
    rand_answ = random.choice(list)
    await message.answer(rand_answ)

@dp.message(Command("photo"))
async def photo(message: Message):
    list = ['https://i.pinimg.com/236x/93/ed/3a/93ed3af6411e1e8b997038c74c287a8a.jpg', 'https://ic.pics.livejournal.com/olegmakarenko.ru/12791732/2404737/2404737_original.jpg',
            'Не отправляйте мне такое больше!', 'Круто!', 'Это очень красивое фото!']
    rand_photo = random.choice(list)
    await message.answer_photo(photo=rand_photo, caption='Ого, какая фотка!')

@dp.message(F.text == "Что такое ИИ?")
async def aitext(message: Message):
    await message.answer('Искусственный интеллект — это свойство искусственных интеллектуальных систем выполнять творческие функции, которые традиционно считаются прерогативой человека; наука и технология создания интеллектуальных машин, особенно интеллектуальных компьютерных программ')


@dp.message(Command("help"))
async def help(message: Message):
    await message.answer("Привет! Я бот, который может отправлять новости. Вот мои команды:\n"
                         "/start - Запустить бота\n"
                         "/weather - Получить последнюю новость\n"
                         "/help - вызов всех команд, которые может выполнять бот\n"
                         "/photo - отправить фото\n"
                         "/react_photo - реагировать на фото")


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Привет, Я бот!")

async def on_startup(_):
    await dp.start_polling(bot)

async def main():
    await on_startup(dp)
    await dp.start_polling(bot)

@dp.message(Command("weather"))
async def weather(message: Message):
    await message.answer(get_weather())


def get_weather(city="Moscow"):
    api_key = "d9a0f4c37c536dec3b20825900c97115"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru"
    response = requests.get(url)
    data = response.json()

    if data.get("cod") != 200:
        return "Ошибка при получении данных о погоде"

    weather = data["weather"][0]["description"]
    temp = data["main"]["temp"]
    return f"Погода в {city}: {weather.capitalize()}, температура: {temp}°C"


if __name__ == "__main__":
    asyncio.run(main())


# my_pal_bot
# best_pal_bot

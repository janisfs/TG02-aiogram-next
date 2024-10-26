import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from config import TOKEN
import random
import requests
from gtts import gTTS
import os


bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command("video"))  # команда для запуска видео
async def video(message: Message):
    await bot.send_chat_action(message.chat.id, "upload_video")
    try:
        video = FSInputFile("tg02-aiogram-test.mp4")
        await bot.send_video(message.chat.id, video)
    except Exception as e:
        await message.answer(f"Ошибка: {e}")

@dp.message(Command("voice"))  # команда озвучивания голосовых сообщений
async def voice(message: Message):
    voice = FSInputFile("multyashnyiy-golos.ogg")
    await message.answer_voice(voice)

@dp.message(Command("doc"))  # команда отправки документа
async def doc(message: Message):
    doc = FSInputFile("payment_report.pdf")
    await bot.send_document(message.chat.id, doc)

@dp.message(Command("audio"))  # команда для запуска аудио
async def audio(message: Message):
    audio = FSInputFile("metro-poezd.mp3")
    await bot.send_audio(message.chat.id, audio)


@dp.message(Command("training"))  # команда для запуска мини рандомной тренировки
async def training(message: Message):
    training_list = [
        "Тренировка 1:\n1. Скручивания: 3 подхода по 15 повторений\n2. Велосипед: 3 подхода по 20 повторений (каждая сторона)\n3. Планка: 3 подхода по 30 секунд",
        "Тренировка 2:\n1. Подъемы ног: 3 подхода по 15 повторений\n2. Русский твист: 3 подхода по 20 повторений (каждая сторона)\n3. Планка с поднятой ногой: 3 подхода по 20 секунд (каждая нога)",
        "Тренировка 3:\n1. Скручивания с поднятыми ногами: 3 подхода по 15 повторений\n2. Горизонтальные ножницы: 3 подхода по 20 повторений\n3. Боковая планка: 3 подхода по 20 секунд (каждая сторона)"
    ]
    rand_training = random.choice(training_list)
    await message.answer(f"Это ваша мини тренировка на сегодня:\n{rand_training}")

    tts = gTTS(text =rand_training, lang='ru')  # Создаем объект gTTS для преобразования текста в аудио
    tts.save("training.ogg")
    audio = FSInputFile("training.ogg")
    await bot.send_audio(message.chat.id, audio)
    os.remove("training.ogg")


@dp.message(F.photo)  # команды реакций на фотографии
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


@dp.message(Command("help"))  # команда для вызова всех команд, которые может выполнять бот
async def help(message: Message):
    await message.answer("Привет! Я бот, который может отправлять новости. Вот мои команды:\n"
                         "/start - Запустить бота\n"
                         "/weather - Получить последнюю новость\n"
                         "/help - вызов всех команд, которые может выполнять бот\n"
                         "/photo - отправить фото\n"
                         "/react_photo - реагировать на фото\n"
                         "/audio - отправить аудио\n"
                         "/video - отправить видео\n"
                         "/training - отправить тренировку\n"
                         "/voice - отправить голосовое сообщение\n"
                         "/doc - отправить документ\n")


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Привет, Я бот!")

async def on_startup(_):
    await dp.start_polling(bot)

async def main():
    await on_startup(dp)
    await dp.start_polling(bot)

@dp.message(Command("weather"))  # команда для вызова погоды в москве
async def weather(message: Message):
    await message.answer(get_weather())


def get_weather(city="Moscow"):
    api_key = "d9a0f4c37c536dec3b20825900c97115"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru"
    timeout = 30  # секунды
    response = requests.get(url, timeout=timeout)
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

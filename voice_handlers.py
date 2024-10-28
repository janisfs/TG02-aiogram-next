from aiogram import F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
import os


def register_voice_handlers(dp, bot):
    # 1. Сохранение голосового сообщения
    @dp.message(F.voice)
    async def save_voice(message: Message):
        print("Получено голосовое сообщение!")  # Отладочный вывод
        try:
            voice = message.voice
            print(f"ID голосового: {voice.file_id}")  # Отладочный вывод

            file = await bot.get_file(voice.file_id)
            print(f"Получена информация о файле: {file.file_path}")  # Отладочный вывод

            # Создаем директорию при сохранении
            os.makedirs("voices", exist_ok=True)
            voice_path = f"voices/voice_{message.from_user.id}_{voice.file_id}.ogg"
            print(f"Попытка сохранить в: {voice_path}")  # Отладочный вывод

            await bot.download_file(file.file_path, voice_path)

            file_size = os.path.getsize(voice_path) / 1024  # размер в КБ
            print(f"""
Информация о сохранении:
- Путь: {voice_path}
- Размер: {file_size:.2f} КБ
- ID пользователя: {message.from_user.id}
- Имя пользователя: {message.from_user.username}
            """)

            await message.answer("Голосовое сообщение сохранено! Используйте команду /send_voice для его отправки")

        except Exception as e:
            print(f"Ошибка при сохранении голосового: {e}")
            print(f"Тип ошибки: {type(e)}")  # Отладочный вывод
            await message.answer("Произошла ошибка при сохранении голосового сообщения")
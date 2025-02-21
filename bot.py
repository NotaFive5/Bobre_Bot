import os
import logging
import requests
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton
import asyncio

# Инициализация логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
API_TOKEN = os.getenv('TELEGRAM_TOKEN')
API_URL = "https://your-server-domain.com/api"

if not API_TOKEN:
    raise ValueError("❌ TELEGRAM_TOKEN не найден! Убедись, что переменная окружения установлена корректно.")

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# URL игры на GitHub Pages
GAME_URL = "https://notafive5.github.io/BoberCurwa/"

# Обработка команды /start
@dp.message(Command("start"))
async def start_command(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username or "unknown"

    # Сохранение данных пользователя на сервере
    try:
        response = requests.post(f"{API_URL}/save_user", json={"user_id": user_id, "username": username})
        if response.status_code == 200:
            await message.answer(f"Привет, {username}! Нажми на ссылку, чтобы играть: [Играть в FLAPPY BOBR]({GAME_URL})", parse_mode="Markdown")
        else:
            await message.answer("Не удалось сохранить данные пользователя. Попробуйте позже.")
    except Exception as e:
        logging.error(e)
        await message.answer("Произошла ошибка при сохранении данных пользователя.")

# Обработка команды /score для отправки очков
@dp.message(Command("score"))
async def send_score(message: Message):
    user_id = message.from_user.id
    try:
        response = requests.get(f'{API_URL}/user_score?user_id={user_id}')
        if response.status_code == 200:
            score = response.json().get('score', 0)
            await message.answer(f'Ваш текущий счёт: {score} очков!')
        else:
            await message.answer('Не удалось получить ваш счёт. Попробуйте позже.')
    except Exception as e:
        logging.error(e)
        await message.answer('Произошла ошибка при получении счёта.')

# Обработка команды /top для отображения таблицы лидеров
@dp.message(Command("top"))
async def send_leaderboard(message: Message):
    try:
        response = requests.get(f'{API_URL}/leaderboard')
        if response.status_code == 200:
            leaderboard = response.json().get('leaderboard', [])
            leaderboard_text = '🏆 Таблица лидеров:\n'
            for idx, entry in enumerate(leaderboard, start=1):
                leaderboard_text += f'{idx}. {entry["username"]}: {entry["score"]} очков\n'
            await message.answer(leaderboard_text)
        else:
            await message.answer('Не удалось загрузить таблицу лидеров. Попробуйте позже.')
    except Exception as e:
        logging.error(e)
        await message.answer('Произошла ошибка при загрузке таблицы лидеров.')

# Запуск бота
async def main():
    dp.include_router(dp)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

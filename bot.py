

import os

from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import Router
import logging
import requests

# Инициализация логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
API_TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# URL игры на GitHub Pages
GAME_URL = "https://notafive5.github.io/BoberCurwa/"
API_URL = "https://your-server-domain.com/api"

# Обработка команды /start
@dp.message_handler(commands=['start'])
async def start_command(message: Message):
    await message.answer(
        f'Привет! Нажми на ссылку, чтобы играть: [Играть в FLAPPY BOBR]({GAME_URL})',
        parse_mode="Markdown"
    )

# Обработка команды /score для отправки очков
@dp.message_handler(commands=['score'])
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
@dp.message_handler(commands=['top'])
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
if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)

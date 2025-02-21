import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
import requests

logging.basicConfig(level=logging.INFO)

API_TOKEN = os.getenv('TELEGRAM_TOKEN')
API_URL = "https://your-server-domain.com/api"
GAME_URL = "https://notafive5.github.io/BoberCurwa/"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer(
        f'Привет! Нажми на ссылку, чтобы играть: [Играть в FLAPPY BOBR]({GAME_URL})',
        parse_mode="Markdown"
    )

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

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

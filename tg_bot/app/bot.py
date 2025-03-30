import logging
from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from app.handlers import user_router


logging.basicConfig(level=logging.INFO)
  
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(user_router)


def get_bot_and_dispatcher():
    return bot, dp
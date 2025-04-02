import logging
from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from app.handlers import routers


logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

for router in routers:
    dp.include_router(router)


def get_bot_and_dispatcher():
    return bot, dp
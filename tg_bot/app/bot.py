import logging
from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from tg_bot.app.handlers import routers


logging.basicConfig(level=logging.INFO)


def get_bot_and_dispatcher():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    for router in routers:
        dp.include_router(router)
    return bot, dp

import asyncio
from app.bot import get_bot_and_dispatcher


async def main():
    bot, dp = get_bot_and_dispatcher()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
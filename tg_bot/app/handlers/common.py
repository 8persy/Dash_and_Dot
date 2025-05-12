from aiogram import Router, types
from aiogram.filters import CommandStart
from tg_bot.app.keyboards.keyboards import get_main_keyboard


common_router = Router()


@common_router.message(CommandStart())
async def process_start_command(message: types.Message):
    await message.answer(
        "Привет, я морзе-бот!\n"
        "Для работы со мной у "
        "тебя есть клавиатура с доступными действиями :)",
        reply_markup=get_main_keyboard()
    )

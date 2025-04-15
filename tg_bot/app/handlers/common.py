from aiogram import Router, types
from aiogram.filters import CommandStart


common_router = Router()


@common_router.message(CommandStart())
async def process_start_command(message: types.Message):
    await message.answer(
        "Привет, я морзе-бот!\n"
        "Доступные команды:\n"
        "/text_to_morse\n"
        "/morse_to_text\n"
        "/text_to_audio\n")

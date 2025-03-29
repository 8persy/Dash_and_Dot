from aiogram import Router, types
from aiogram.filters import CommandStart

router = Router()


@router.message(CommandStart())
async def process_start_command(message: types.Message):
    await message.answer("Привет, я эхо-бот! Отправь мне текстовое сообщение, и я повторю его.")


@router.message(lambda msg: msg.text)
async def process_echo_message(message: types.Message):
    await message.answer(message.text)


@router.message()
async def process_not_text_message(message: types.Message):
  await message.answer("Извини, я не понимаю тебя :(")
# handlers/audio.py
from aiogram import Router, types
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from io import BytesIO
import tempfile
import os

from morse.morse import MorseCode
from tg_bot.app.states.morse_states import MorseStates
from tg_bot.app.keyboards.keyboards import get_main_keyboard

audio_router = Router()


@audio_router.message(
        StateFilter(None), lambda msg: msg.text == "Аудио в текст"
)
async def cmd_audio_to_text(message: types.Message, state: FSMContext):
    await message.answer(
        "Отправь мне аудиофайл (.wav или .mp3), "
        "содержащий код Морзе, и я переведу его в текст.",
        reply_markup=get_main_keyboard()
    )
    await state.set_state(MorseStates.audio_to_text)


@audio_router.message(MorseStates.audio_to_text)
async def process_audio_to_text(message: Message, state: FSMContext):
    processing_msg = await message.answer("Обрабатываю аудиофайл...🔍")

    file = message.audio or message.voice or message.document
    if file is None:
        await message.answer(
            "Пожалуйста, отправь аудиофайл в формате MP3 или WAV."
        )
        return

    try:
        # Получаем file_id и загружаем файл через bot
        file_id = file.file_id
        telegram_file = await message.bot.get_file(file_id)

        file_bytes = BytesIO()
        await message.bot.download_file(
            telegram_file.file_path, destination=file_bytes
        )
        file_bytes.seek(0)

        # Определяем расширение
        filename = getattr(file, 'file_name', None) or 'voice.ogg'
        suffix = (
            '.mp3' if filename.endswith('.mp3') else
            '.wav' if filename.endswith('.wav') else
            '.ogg'
        )

        # Сохраняем во временный файл
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as temp:
            temp.write(file_bytes.read())
            temp_file_path = temp.name

        # Декодируем
        if suffix == '.mp3':
            decoded = MorseCode.from_mp3file(temp_file_path).decode()
        else:
            decoded = MorseCode.from_wavfile(temp_file_path).decode()

        os.remove(temp_file_path)

        await processing_msg.edit_text(
            f"Текст из аудио:\n<code>{decoded}</code>",
            parse_mode='HTML'
        )
        await state.clear()

    except Exception as e:
        await message.answer(
            "Произошла ошибка при обработке аудиофайла."
        )
        print(f"Error: {e}")
        await state.clear()

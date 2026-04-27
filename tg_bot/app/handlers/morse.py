import os
import soundfile as sf
import tempfile


from aiogram import Router, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from tg_bot.app.services.morse import (text_to_morse,
                                       morse_to_text,
                                       generate_morse_audio)

from tg_bot.app.states.morse_states import MorseStates
from tg_bot.app.keyboards.keyboards import get_main_keyboard


morse_router = Router()


@morse_router.message(
        StateFilter(None), lambda msg: msg.text == "Текст в Морзе"
)
async def cmd_text_to_morse(message: types.Message, state: FSMContext):
    await message.answer(
        "Отправь мне текст на английском, и я переведу его в код Морзе.\n"
    )
    await state.set_state(MorseStates.waiting_for_text)


@morse_router.message(MorseStates.waiting_for_text)
async def process_text_to_morse_cmd(message: types.Message, state: FSMContext):
    text = message.text

    try:
        morse_text = text_to_morse(text)
        await message.answer(
            f"Код Морзе:\n<code>{morse_text}</code>",
            parse_mode='HTML',
            reply_markup=get_main_keyboard()
        )
        await state.clear()
    except Exception as e:
        await message.answer(
            "Произошла ошибка при переводе в код Морзе",
            reply_markup=get_main_keyboard()
        )
        print(f"Error: {e}")
        await state.clear()


@morse_router.message(
        StateFilter(None), lambda msg: msg.text == "Морзе в текст"
)
async def cmd_morse_to_text(message: types.Message, state: FSMContext):
    await message.answer(
        "Отправь мне код Морзе, и я переведу его на английский язык.\n"
    )
    await state.set_state(MorseStates.waiting_for_morse)


@morse_router.message(MorseStates.waiting_for_morse)
async def process_morse_to_text_cmd(message: types.Message, state: FSMContext):
    text = message.text

    try:
        english_text = morse_to_text(text)
        await message.answer(
            f"Текст на английском:\n<code>{english_text}</code>",
            parse_mode='HTML',
            reply_markup=get_main_keyboard()
        )
        await state.clear()
    except Exception as e:
        await message.answer(
            "Произошла ошибка при переводе",
            reply_markup=get_main_keyboard()
        )
        print(f"Error: {e}")
        await state.clear()


@morse_router.message(
        StateFilter(None), lambda msg: msg.text == "Текст в аудио"
)
async def cmd_text_to_audio(message: types.Message, state: FSMContext):
    await message.answer(
        "Отправь мне текст на английском, "
        "и я пришлю тебе аудио файл с его Морзе кодом.\n"
    )
    await state.set_state(MorseStates.text_to_audio)


@morse_router.message(MorseStates.text_to_audio)
async def process_text_to_audio_cmd(message: types.Message, state: FSMContext):
    text = message.text

    try:
        morse_text = text_to_morse(text)

        with tempfile.TemporaryDirectory() as temp_dir:
            audio = generate_morse_audio(text=text)
            file_path = os.path.join(temp_dir, 'morse.wav')
            sf.write(file_path, audio, 8000)

            audio_file = FSInputFile(file_path)
            await message.answer(
                f"Код Морзе:\n<code>{morse_text}</code>",
                parse_mode='HTML',
                reply_markup=get_main_keyboard()
            )
            await message.answer_audio(
                audio_file,
                caption="Аудио версия кода Морзе"
            )

    except Exception as e:
        await message.answer(
            "Произошла ошибка при переводе в аудио",
            reply_markup=get_main_keyboard()
        )
        print(f"Error: {e}")
    finally:
        await state.clear()

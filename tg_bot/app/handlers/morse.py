from aiogram import Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from app.services.morse import text_to_morse
from app.states.morse_states import MorseStates


morse_router = Router()

@morse_router.message(StateFilter(None), Command('text_to_morse'))
async def cmd_morse(message: types.Message, state: FSMContext):
    await message.answer(
        "Отправь мне текст на английском, и я переведу его в код Морзе.\n"
    )
    await state.set_state(MorseStates.waiting_for_text)

@morse_router.message(MorseStates.waiting_for_text)
async def process_morse_command(message: types.Message, state: FSMContext):
    text = message.text

    try:
        morse_text = text_to_morse(text)
        await message.answer(f"Код Морзе:\n<code>{morse_text}</code>", parse_mode='HTML')
        await state.clear()
    except Exception as e:
        await message.answer("Произошла ошибка при переводе в код Морзе")
        print(f"Error: {e}")
        await state.clear()
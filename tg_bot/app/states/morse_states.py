from aiogram.fsm.state import State, StatesGroup


class MorseStates(StatesGroup):
    waiting_for_text = State()
    waiting_for_morse = State()

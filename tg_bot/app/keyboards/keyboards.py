from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_keyboard() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text="Текст в Морзе")],
        [KeyboardButton(text="Морзе в текст")],
        [KeyboardButton(text="Текст в аудио")],
        [KeyboardButton(text="Аудио в текст")],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )

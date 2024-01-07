from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=
        [
            [
                KeyboardButton(text='Записать в кассу ✏️')
            ]
        ], resize_keyboard=True, one_time_keyboard=True
    )


async def operation_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=
        [
            [
                KeyboardButton(text='Приход 🟢'),
                KeyboardButton(text='Расход 🔴')
            ]
        ], resize_keyboard=True, one_time_keyboard=True
    )

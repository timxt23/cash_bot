from typing import List
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def kb_inline_date(dates: list):
    """Клавиатора выбора дат 3х дней"""
    date_list: List[InlineKeyboardButton] = []
    buttons: List = []

    for el_date in dates:
        if len(date_list) == 3:
            buttons.append(date_list)
            date_list = []

        button = InlineKeyboardButton(
            text=el_date,
            callback_data=f"dates_choice={el_date}"
        )

        date_list.append(button)

    buttons.append(date_list)
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def kb_inline_warehouse(results: list):
    """Клавиатура выбора складов"""
    warehouse_list : List[InlineKeyboardButton] = []
    buttons: List = []

    for el_wh in results:
        button = InlineKeyboardButton(
            text=el_wh,
            callback_data=f"wh_choice={el_wh}"
        )
        warehouse_list.append(button)

    buttons.append(warehouse_list)
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def kb_inline_confirmation():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                text="Отменить ⛔️",
                callback_data="confirmation=canceled"
                ),
                InlineKeyboardButton(
                    text="Подтвердить ✅",
                    callback_data="confirmation=accepted"
                )
            ]
        ]
    )
    return keyboard


async def kb_inline_again():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Сделать новую запись",
                    callback_data="again_choice=new_record"
                )
            ]
        ]
    )
    return keyboard

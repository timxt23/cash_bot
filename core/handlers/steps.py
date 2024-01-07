import re
import os
import json
from dotenv import load_dotenv

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.keyboards import std_kb, inline_kb
from core.keyboards.inline_kb import kb_inline_warehouse, kb_inline_confirmation
from core.others.get_date import get_dates
from core.others.get_warehouse import get_wh_names
from core.others.states_user import States
from core.others.write_gsheet import write_new_op

load_dotenv()

router = Router()

users_data = json.loads(os.environ["USERS"])
users = [int(i) for i in users_data.values()]


@router.message(Command(commands=['start', 'new_operation']))
async def get_menu(message: Message, state: FSMContext):
    if message.from_user.id in users:
        await message.answer(
            f"Привет <b>{message.from_user.first_name}</b>, я кассовый бот Крис 🤖.\n"
            "Я помогу тебе заполнять кассу прямо отсюда.🤑📆",
            reply_markup=await std_kb.main_keyboard()
        )
    else:
        await message.answer('C незнакомцами не говорю')


@router.message(F.text == 'Записать в кассу ✏️')
async def get_operation(message: Message, state: FSMContext):
    await message.answer(
        f"Начнем. Выбери <b>тип операции</b>:",
        reply_markup=await std_kb.operation_keyboard()
    )
    await state.set_state(States.state_choice)


@router.callback_query(States.state_confirmation)
async def get_confirmation(call: CallbackQuery, state: FSMContext):
    data_called = call.data.split('=')[1]
    if data_called == "canceled":
        await call.message.edit_text('Отменено...')
        await state.clear()
    else:
        data = await state.get_data()
        result = await write_new_op(data)
        if result is True:
            await call.message.edit_text(
                f"✅ Записано в таблицу \r\n\n"
                f"Тип:  <b>{data['type']}</b>\r\n"
                f"📅 Дата:  <b>{data['date']}</b>\r\n"
                f"💸 Cумма:  <b>{data['amount']}</b> руб.\r\n"
                f"📝 Комментарий:  <b>{data['comment']}</b>\r\n"
                f"💁🏻‍ Склад/лицо:  <b>{data['warehouse']}</b>"
            )
            await call.message.answer(
                f"Готово!",
                reply_markup=await std_kb.main_keyboard()
            )
            await state.set_state(States.state_confirmed)


@router.callback_query(States.state_subject)
async def get_op_warehouse(call: CallbackQuery, state: FSMContext):
    data_called = call.data.split('=')[1]
    data = await state.get_data()
    await state.update_data(warehouse=data_called)
    await call.message.edit_text(
        f"Тип:  <b>{data['type']}</b>\r\n"
        f"📅 Дата:  <b>{data['date']}</b>\r\n"
        f"💸 Cумма:  <b>{data['amount']}</b> руб.\r\n"
        f"📝 Комментарий:  <b>{data['comment']}</b>\r\n"
        f"💁🏻‍ Склад/лицо:  <b>{data_called}</b>",
        reply_markup=await kb_inline_confirmation()
    )

    await state.set_state(States.state_confirmation)


@router.message(States.state_search_wh)
async def get_op_search_result(message: Message, state: FSMContext):
    search_result = await get_wh_names(message.text)
    if len(search_result) == 0:
        await message.reply(f"Проверь запрос и попробуй снова")

    else:
        await message.answer(
            f"Найдено: <b>{len(search_result)}</b>\r\n"
            f"Выберете склад ниже:",
            reply_markup=await kb_inline_warehouse(search_result)
        )
        await state.set_state(States.state_subject)


@router.message(States.state_comment)
async def get_op_comment(message: Message, state: FSMContext):
    await message.answer(
        f"Коммент: {message.text}\r\n"
        f"Введите мин. 3 буквы склада 🏭:"
    )
    await state.update_data(comment=message.text)
    await state.set_state(States.state_search_wh)


@router.message(States.state_amount)
async def get_op_amount(message: Message, state: FSMContext):
    result = re.match(r'^(\-)?\d+(\,\d{1,2})?$', message.text)

    if not result:
        return await message.answer('Сумма на соответствует формату')

    await message.answer(
        f"Cумма: <b>{message.text}</b> руб.\r\nНапишите комментарий:"
    )
    await state.update_data(amount=message.text)
    await state.set_state(States.state_comment)


@router.callback_query(States.state_date)
async def set_op_date(call: CallbackQuery, state: FSMContext):
    data_called = call.data.split('=')[1]
    data = await state.get_data()
    type_needed = data['type']
    await call.message.edit_text(
        f"Тип: <b>{type_needed}</b>\r\n"
        f"Выбранная дата: <b>{data_called}</b>,\r\n"
        f"Укажите сумму в рублях 💸:"
    )

    await state.set_state(States.state_amount)
    await state.update_data(date=data_called)


@router.message(States.state_choice)
async def get_op_date(message: Message, state: FSMContext):
    await state.update_data(user=message.from_user.id)
    dates = reversed(get_dates())  # Получаем 3 даты предыдущего дня
    await message.answer(
        f"📅 Выберите дату операции:",
        reply_markup=await inline_kb.kb_inline_date(dates)
    )
    await state.update_data(type=message.text.split(' ')[0])
    await state.set_state(States.state_date)


@router.message(States.state_confirmed)
async def make_op_again(message: Message, state: FSMContext):
    await state.clear()
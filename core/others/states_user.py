from aiogram.fsm.state import StatesGroup, State


class States(StatesGroup):
    state_cashier = State()
    state_choice = State()
    state_date = State()
    state_amount = State()
    state_comment = State()
    state_search_wh = State()
    state_subject = State()
    state_confirmation = State()
    state_confirmed = State()

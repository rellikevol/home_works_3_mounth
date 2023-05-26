from aiogram.dispatcher.filters.state import State, StatesGroup

class SignUpState(StatesGroup):
    name = State()
    tel = State()
    email = State()
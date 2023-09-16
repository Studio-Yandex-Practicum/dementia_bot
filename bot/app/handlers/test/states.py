from aiogram.filters.state import StatesGroup, State


class Register(StatesGroup):
    name = State()
    age = State()
    gender = State()
    email = State()

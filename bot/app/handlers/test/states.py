from aiogram.filters.state import State, StatesGroup


class Register(StatesGroup):
    name = State()
    age = State()
    gender = State()
    email = State()


class Question(StatesGroup):
    test = State()
    answer = State()

from aiogram.fsm.state import State, StatesGroup


class Register(StatesGroup):
    name = State()
    age = State()
    gender = State()
    email = State()
    occupation = State()


class Test(StatesGroup):
    choose_test = State()
    register_participant = Register
    answers = State()

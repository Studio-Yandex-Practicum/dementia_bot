from aiogram.filters.state import State, StatesGroup


class Register(StatesGroup):
    """
    States for user registration process.

    States:
    - name: Collecting user's name.
    - age: Collecting user's age.
    - gender: Collecting user's gender.
    - email: Collecting user's email.
    """
    name = State()
    age = State()
    gender = State()
    email = State()


class Question(StatesGroup):
    """
    States for handling test questions.

    States:
    - test: Selecting a test.
    - answer: Answering questions in the test.
    """
    test = State()
    answer = State()

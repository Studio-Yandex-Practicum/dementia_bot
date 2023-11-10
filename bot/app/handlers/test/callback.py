from enum import Enum

from aiogram.filters.callback_data import CallbackData


class Action(str, Enum):
    """
    Enum class for representing possible actions in callbacks.

    Values:
    - yes: Represents "Да".
    - no: Represents "Нет".
    - sometimes: Represents "Иногда".
    - further: Represents "Далее".
    """
    yes = "Да"
    no = "Нет"
    sometimes = "Иногда"
    further = "Далее"


class AnswerCallback(CallbackData, prefix="answer"):
    """
    CallbackData class for handling answer callbacks.

    Attributes:
    - action: Represents an action from the Action enum.
    """

    action: Action


class Sex(str, Enum):
    """
    Enum class for representing gender values.

    Values:
    - male: Represents "Мужской".
    - female: Represents "Женский".
    """

    male = "Мужской"
    female = "Женский"


class SexCallback(CallbackData, prefix="sex"):
    """
    CallbackData class for handling gender callbacks.

    Attributes:
    - action: Represents a gender value from the Sex enum.
    """
    action: Sex

from enum import Enum

from aiogram.filters.callback_data import CallbackData


class Action(str, Enum):
    yes = "Да"
    no = "Нет"
    sometimes = "Иногда"
    further = "Далее"


class AnswerCallback(CallbackData, prefix="answer"):
    action: Action


class Sex(str, Enum):
    male = "Мужской"
    female = "Женский"


class SexCallback(CallbackData, prefix="sex"):
    action: Sex

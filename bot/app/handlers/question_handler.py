from datetime import datetime

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, KeyboardButton, Message,
                           ReplyKeyboardMarkup, ReplyKeyboardRemove)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from validate_email import validate_email

from app.handlers.handler_constants import PERSONAL_TYPES, GENDER_CHOICES
from app.handlers.test.states import Question
from app.handlers.validators.validator import (validate_birthday,
                                               validate_gender,
                                               validate_bool_answer)
from core.config import settings
from utils.http_client import HttpClient

tests = [
    {
        'name': "test1",
        'id': 1
    },
    {
        'name': "test2",
        'id': 2
    },
    {
        'name': "test3",
        'id': 3
    },

]


question_router = Router()


@question_router.message(Command("cancel"))
@question_router.message(F.text.casefold() == "отмена")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """Allow user to cancel any action."""
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer(
        "Cancelled.",
        reply_markup=ReplyKeyboardRemove(),
    )


@question_router.message(Command('starttest'))
async def start_test(message: Message, state: FSMContext):
    # Tут получаем список Тестов
    await state.set_state(Question.test)
    await message.answer(
        "Выберите тест:",
        reply_markup=inline_builder(tests).as_markup()
    )


@question_router.callback_query(Question.test)
async def choose_test(query: CallbackQuery, state: FSMContext):
    test_id = 1  # пока примем 1, далее будет браться из списка тестов
    async with HttpClient() as session:
        response = await session.get(f'{settings.HOST}api/test/{test_id}/')
    await state.update_data(testId=test_id)
    position = 0
    questions = response['questions']   # Тут получаем список вопросов
    await state.set_state(Question.answer)
    await state.update_data(questions=questions,
                            telegram_id=query.from_user.id)
    await query.message.delete()
    await query.message.answer(
        questions[0]['question'],
        reply_markup=markup_keyboard(questions[0]['type'])
    )
    await state.update_data(position=position)


@question_router.message(Question.answer)
async def questions(message: Message, state: FSMContext):
    data = await state.get_data()
    position = data.get('position')
    questions = data.get('questions')
    type = questions[position]['type']
    answer = message.text
    if type == "multiple_choice":
        if not validate_bool_answer(answer):
            await message.answer(
                "Введите Да или Нет или воспользуйтесь клавиатурой."
            )
            return
    elif type in PERSONAL_TYPES:
        if type == 'birthdate':
            if not validate_birthday(answer):
                await message.answer(
                    "Пожалуйста введите дату рождения в формате ДД.ММ.ГГГГ."
                )
                return
            answer = str(datetime.strptime(answer, '%d.%m.%Y').date())
        elif type == 'gender':
            if not validate_gender(answer):
                await message.answer(
                    "Ваш ответ не соответствует вариантам Мужской/Женский."
                )
                return
            answer = GENDER_CHOICES[answer]
        elif type == 'email':
            if not validate_email(answer):
                await message.answer('Почта неверно написана. Попробуй снова.')
                return
    await state.update_data({f"answer_{position}": answer})
    new_position = position + 1
    if questions[new_position]['type'] == "telegram_id":
        await state.update_data(
            {f"answer_{new_position}": data.get('telegram_id')}
        )
        new_position += 1
    await state.update_data(position=new_position)
    if new_position > len(questions)-1:
        updated_data = await state.get_data()
        json_data = prepare_answers(updated_data)
        async with HttpClient() as session:
            response = await session.post(f'{settings.HOST}api/submit/',
                                          json_data)
        await message.answer(
            "Спасибо за то, что прошли наш тест.",
            reply_markup=ReplyKeyboardRemove(),
        )
        await state.clear()

    else:
        await message.answer(
            questions[new_position]['question'],
            reply_markup=markup_keyboard(
                questions[new_position]['type']
            )
        )


def inline_builder(tests: list):
    builder = InlineKeyboardBuilder()
    for test in tests:
        builder.button(text=test['name'], callback_data=str(test['id']))
    builder.adjust(1, 1)
    return builder


def markup_keyboard(type):
    if type == "multiple_choice":
        markup = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Да"),
                    KeyboardButton(text="Нет")
                ],
                [
                    KeyboardButton(text='Отмена'),
                ],
            ],
            resize_keyboard=True
        )
    else:
        markup = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text='Отмена'),
                ],
            ],
            resize_keyboard=True
        )
    return markup


def prepare_answers(data: dict):
    questions = data.get('questions')
    test_id = data.get('testId')
    json_data = {"testId": test_id,
                 "questions": []}
    for n in range(0, len(questions)):
        answer = {
            "questionId": questions[n]['questionId'],
            "type": questions[n]['type'],
            "answer": data.get(f'answer_{n}')
        }
        json_data['questions'].append(answer)

    return json_data

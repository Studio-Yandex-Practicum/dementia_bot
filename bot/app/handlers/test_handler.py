from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, Message,
                           ReplyKeyboardRemove)

from app.handlers.handler_constants import PERSONAL_TYPES
from app.handlers.keyboards.keyboard import inline_builder, markup_keyboard
from app.handlers.states.states import Test
from app.handlers.validators.validator import validate_bool_answer
from core.config import settings
from utils.http_client import HttpClient


question_router = Router()


@question_router.message(Command('starttest'))
async def start_test(message: Message, state: FSMContext):
    """Получаем список тестов и отправляем пользователю на выбор."""
    async with HttpClient() as session:
        tests = await session.get(f'{settings.HOST}api/tests/')
    await state.set_state(Test.choose_test)
    await message.answer(
        "Выберите тест:",
        reply_markup=inline_builder(tests).as_markup()
    )


@question_router.callback_query(Test.choose_test)
async def choose_test(query: CallbackQuery, state: FSMContext):
    test_id = query.data
    async with HttpClient() as session:
        response = await session.get(f'{settings.HOST}api/test/{test_id}/')
    await state.update_data(testId=test_id)
    position = 0
    questions = response['questions']
    await state.update_data(questions=questions,
                            telegram_id=query.from_user.id,
                            position=position)
    await query.message.delete()
    await state.set_state(Test.register_participant.name)
    await query.message.answer("Введите Имя респондента:")


@question_router.message(Test.answers)
async def questions(message: Message, state: FSMContext):
    data = await state.get_data()
    position = data.get('position')
    questions = data.get('questions')
    question_type = questions[position]['type']
    answer = message.text
    if question_type == "multiple_choice":
        if not validate_bool_answer(answer):
            await message.answer(
                "Введите Да или Нет или воспользуйтесь клавиатурой."
            )
            return
    await state.update_data({f"answer_{position}": answer})
    new_position = position + 1
    await state.update_data(position=new_position)
    if new_position > len(questions)-1:
        updated_data = await state.get_data()
        test_data = prepare_data(updated_data)
        async with HttpClient() as session:
            response = await session.post(f'{settings.HOST}api/submit/',
                                          test_data)
        print(test_data)
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


def prepare_data(data: dict):
    test_id = data.get('testId')
    prepared_data = {"testId": test_id,
                     'questions': prepare_answers(data),
                     'participant': prepare_participant_data(data)}
    return prepared_data


def prepare_answers(data: dict):
    questions = data.get('questions')
    question_list = []
    for n in range(0, len(questions)):
        answer = {
            "questionId": questions[n]['questionId'],
            "type": questions[n]['type'],
            "answer": data.get(f'answer_{n}')
        }
        question_list.append(answer)
    return question_list


def prepare_participant_data(data: dict):
    participant_data = {}
    for type in PERSONAL_TYPES:
        if data.get(type):
            participant_data[type] = data.get(type)
        else:
            participant_data[type] = None
    return participant_data
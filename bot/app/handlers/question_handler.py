from datetime import datetime

from aiogram import F, Router, Bot
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, KeyboardButton, Message,
                           ReplyKeyboardMarkup, ReplyKeyboardRemove)

from app.handlers.handler_constants import PERSONAL_TYPES, GENDER_CHOICES
from app.handlers.test.states import Question
from app.handlers.test.keyboard import (markup_keyboard,
                                        prepare_answers,
                                        inline_builder)
from app.handlers.test.test_result import tests_result
from app.handlers.validators.validator import (validate_birthday,
                                               validate_gender,
                                               validate_bool_answer,
                                               validate_score,
                                               validate_email_address,
                                               validate_current_day)
from core.config import settings
from utils.http_client import HttpClient

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


@question_router.message(Command('selecttest'))
async def start_test(message: Message, state: FSMContext):
    async with HttpClient() as session:
        response = await session.get(
            f'{settings.HOST}api/tests')
    tests = response

    await state.set_state(Question.test)
    await message.answer(
        "Выберите тест:",
        reply_markup=inline_builder(tests).as_markup()
    )


@question_router.callback_query(Question.test)
async def choose_test(query: CallbackQuery, state: FSMContext):
    test_id = int(query.data)
    async with HttpClient() as session:
        response = await session.get(f'{settings.HOST}api/test/{test_id}/')
    await state.update_data(testId=test_id)
    position = 0
    questions = response['questions']
    await state.set_state(Question.answer)
    await state.update_data(questions=questions,
                            telegram_id=query.from_user.id)
    await query.message.delete()
    await query.message.answer(
        questions[0]['question'],
        reply_markup=markup_keyboard(questions[0]['type'])
    )
    await state.update_data(position=position)


@question_router.callback_query(Question.answer)
@question_router.message(Question.answer)
async def questions(message: Message, state: FSMContext):
    data = await state.get_data()
    position = data.get('position')
    questions = data.get('questions')
    type = questions[position]['type']
    answer = message.text
    message_id = message.message_id
    print(message.chat.id)
    chat_id = message.chat.id

    if type == "multiple_choice":
        if not validate_bool_answer(answer):
            await message.answer(
                reply_markup=markup_keyboard(questions[position]['type']).as_markup()
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
                    "Ваш ответ не соответствует вариантам Мужской/Женский.",
                    reply_markup=markup_keyboard(questions[position]['type'])
                )
                return
            answer = GENDER_CHOICES.get(answer)
        elif type == 'email':
            if not validate_email_address(answer):
                await message.answer('Почта неверно написана. Попробуй снова.')
                return
        elif questions[position]['type'] == 'current_day':
            if not validate_current_day(answer):
                await message.answer(
                    "Пожалуйста, введите текущий день недели ДД.ММ.ГГГГ :"
                )
                return
    await state.update_data({f"answer_{position}": answer})

    new_position = position + 1

    if new_position < len(questions):
        if questions[new_position]['type'] == "telegram_id":
            await state.update_data(
                {f"answer_{new_position}": data.get('telegram_id')}
            )
            new_position += 1

    if new_position >= len(questions):
        # Вопросы закончились, можно завершить тест
        updated_data = await state.get_data()
        json_data = prepare_answers(updated_data)
        async with HttpClient() as session:
            response = await session.post(f'{settings.HOST}api/submit/',
                                          json_data)

        finish_markup = ReplyKeyboardRemove()  # Убрать клавиатуру

        telegram_id = message.from_user.id
        async with HttpClient() as session:
            response = await session.get(
                f'{settings.HOST}api/get_result/{telegram_id}/')

        result_data = response
        result = result_data['result']
        result_test = result_data['test']
        tests_result(result_test, result)

        await message.answer(tests_result(result_test, result))

        await state.clear()
    else:
        await state.update_data(position=new_position)
        await message.delete()
        await message.delete_message(chat_id, message_id)
        await message.answer(
            questions[new_position]['question'],
            reply_markup=markup_keyboard(questions[new_position]['type'])
        )

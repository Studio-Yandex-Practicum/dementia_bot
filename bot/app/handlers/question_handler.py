from datetime import datetime

from aiogram import F, Router, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, Message, ReplyKeyboardRemove)

from app.handlers.handler_constants import PERSONAL_TYPES, GENDER_CHOICES, \
    START_MESSAGE
from app.handlers.test.states import Question
from app.handlers.test.keyboard import (markup_keyboard,
                                        prepare_answers,
                                        inline_builder,
                                        answer_keyboarder,
                                        sex_keyboarder,
                                        triple_answer_keyboarder,
                                        further_keyboarder)
from app.handlers.test.callback import AnswerCallback, Action, SexCallback, Sex
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


async def display_question(chat_id, message_id, question_text, question_type,
                           bot):
    """Отобразить вопрос с клавиатурой в зависимости от типа."""
    keyboard = None

    if question_type == 'gender':
        keyboard = sex_keyboarder()
    elif question_type == 'multiple_choice':
        keyboard = answer_keyboarder()
    elif question_type == 'triple_choice':
        keyboard = triple_answer_keyboarder()
    elif question_type == 'inline_button':
        keyboard = further_keyboarder()

    if keyboard is not None:
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=question_text,
            reply_markup=keyboard
        )
    else:
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=question_text,
            reply_markup=None
        )


async def send_results_and_clear(state, bot, chat_id, message_id):
    """Отправить результаты и очистить состояние."""
    updated_data = await state.get_data()
    json_data = prepare_answers(updated_data)

    async with HttpClient() as session:
        response = await session.post(f'{settings.HOST}api/submit/', json_data)

    telegram_id = updated_data.get('telegram_id')
    async with HttpClient() as session:
        response = await session.get(
            f'{settings.HOST}api/get_result/{telegram_id}/')

    result_data = response
    result = result_data['result']
    result_test = result_data['test']

    await bot.edit_message_text(chat_id=chat_id,
                                message_id=message_id,
                                text=tests_result(result_test, result))

    await state.clear()

@question_router.message(Command("cancel"))
@question_router.message(F.text.casefold() == "отмена")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """Позволяет пользователю отменить любое действие."""
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
    """Начать тест, показывая список доступных тестов."""
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
    """Выбрать тест и начать отвечать на вопросы."""
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
    await state.update_data(message_id=query.message.message_id + 1)
    await state.update_data(position=position)


@question_router.message(Question.answer)
async def questions(message: Message, state: FSMContext, bot: Bot):
    """Обработка ответов на вопросы в тесте."""
    data = await state.get_data()
    position = data.get('position')
    message_id = data.get('message_id')
    questions = data.get('questions')
    type = questions[position]['type']
    answer = message.text
    chat_id = message.chat.id

    if type in PERSONAL_TYPES:
        if type == 'birthdate':
            if not validate_birthday(answer):
                await message.answer(
                    "Пожалуйста введите дату рождения в формате ДД.ММ.ГГГГ."
                )
                return
            answer = str(datetime.strptime(answer, '%d.%m.%Y').date())
        elif type == 'email':
            if not validate_email_address(answer):
                await message.answer('Почта неверно написана. Попробуй снова.')
                return
        elif questions[position]['type'] == 'current_day':
            if not validate_current_day(answer):
                await message.answer(
                    "Пожалуйста, введите текущий день недели ДД.ММ.ГГГГ."
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

        await send_results_and_clear(state, bot, chat_id, message_id)

    else:
        await state.set_state(Question.answer)
        await state.update_data(position=new_position)
        new_question_text = questions[new_position]['question']
        question_type = questions[new_position]['type']
        await display_question(chat_id, message_id, new_question_text, question_type, bot)
        await message.delete()


@question_router.callback_query(
    AnswerCallback.filter(F.action.in_(
        [Action.yes, Action.no, Action.sometimes, Action.further])))
async def answer_handler(query: CallbackQuery, callback_data: AnswerCallback,
                         state: FSMContext, bot: Bot):
    """Обработка ответов с использованием кнопок с действиями."""
    data = await state.get_data()
    position = data.get('position')
    questions = data.get('questions')
    message_id = query.message.message_id
    chat_id = query.message.chat.id

    if callback_data.action == Action.yes:
        answer = 'Да'
    elif callback_data.action == Action.no:
        answer = 'Нет'
    elif callback_data.action == Action.sometimes:
        answer = 'Иногда'
    else:
        answer = 'Принято'

    await state.update_data({f"answer_{position}": answer})

    new_position = position + 1
    if new_position < len(questions):
        if questions[new_position]['type'] == "telegram_id":
            await state.update_data(
                {f"answer_{new_position}": data.get('telegram_id')}
            )
            new_position += 1

    if new_position >= len(questions):
        await send_results_and_clear(state, bot, chat_id, message_id)
    else:
        await state.update_data(position=new_position)
        new_question_text = questions[new_position]['question']
        question_type = questions[new_position]['type']
        await display_question(chat_id, message_id, new_question_text, question_type, bot)



@question_router.callback_query(
    SexCallback.filter(F.action.in_([Sex.male, Sex.female])))
async def sex_handler(query: CallbackQuery, callback_data: SexCallback,
                      state: FSMContext, bot: Bot):
    """Обработка выбора пола."""
    data = await state.get_data()
    position = data.get('position')
    questions = data.get('questions')
    message_id = data.get('message_id')
    chat_id = query.message.chat.id
    if callback_data.action == Sex.male:
        answer = 'Мужской'
    else:
        answer = 'Женский'
    answer = GENDER_CHOICES[answer]
    await state.update_data({f"answer_{position}": answer})

    new_position = position + 1

    await state.update_data(position=new_position)
    new_question_text = questions[new_position]['question']
    question_type = questions[new_position]['type']
    await display_question(chat_id, message_id, new_question_text,
                           question_type, bot)

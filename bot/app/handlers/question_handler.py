from datetime import datetime

from aiogram import F, Router, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, Message, ReplyKeyboardRemove)

from app.handlers.handler_constants import PERSONAL_TYPES, GENDER_CHOICES, \
    START_MESSAGE
from app.handlers.test.states import Question
from app.handlers.test.keyboard import (prepare_answers,
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
    """
    Display a question with a keyboard based on its type.

    Args:
    - chat_id: ID of the chat.
    - message_id: ID of the message.
    - question_text: Text of the question.
    - question_type: Type of the question.
    - bot: Bot instance.
    """
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


@question_router.message(Command("cancel"))
@question_router.message(F.text.casefold() == "отмена")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Allow the user to cancel any action.

    Args:
    - message: The message object.
    - state: The FSMContext object.
    """
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
    """
    Start a test, showing the list of available tests.

    Args:
    - message: The message object.
    - state: The FSMContext object.
    """
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
    """
    Choose a test and start answering questions.

    Args:
    - query: The CallbackQuery object.
    - state: The FSMContext object.
    """
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
        reply_markup=None
    )
    await state.update_data(message_id=query.message.message_id + 1)
    await state.update_data(position=position)


@question_router.message(Question.answer)
async def questions(message: Message, state: FSMContext, bot: Bot):
    """
    Process answers to questions in the test.

    Args:
    - message: The Message object.
    - state: The FSMContext object.
    - bot: Bot instance.
    """
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
                await message.delete()
                return
            answer = str(datetime.strptime(answer, '%d.%m.%Y').date())
        elif type == 'email':
            if not validate_email_address(answer):
                await message.answer('Почта неверно написана. Попробуй снова.')
                await message.delete()
                return
        elif questions[position]['type'] == 'current_day':
            if not validate_current_day(answer):
                await message.answer(
                    "Пожалуйста, введите текущий день недели ДД.ММ.ГГГГ."
                )
                await message.delete()
                return
    await state.update_data({f"answer_{position}": answer})

    new_position = position + 1
    new_position = await update_data_telegram_id(state, new_position)

    if new_position >= len(questions):

        await send_results_and_clear(state, bot, chat_id, message_id)

    else:
        await state.set_state(Question.answer)
        await state.update_data(position=new_position)
        new_question_text = questions[new_position]['question']
        question_type = questions[new_position]['type']
        await display_question(chat_id, message_id, new_question_text,
                               question_type, bot)
        await message.delete()


async def update_data_telegram_id(state, position):
    """
    Update data with 'telegram_id' answer at the given position if applicable.

    Args:
    - state: The FSMContext object.
    - position: The current position in the questions list.

    Returns:
    - int: The updated position.
    """
    data = await state.get_data()
    questions = data.get('questions')

    if position < len(questions) and questions[position]['type'] == "telegram_id":
        await state.update_data(
            {f"answer_{position}": data.get('telegram_id')})
        return position + 1

    return position


async def handle_callback_query_action(query, callback_data, state, bot,
                                       action_mapping):
    """
    Handle callback query actions and update the state accordingly.

    Args:
    - query: The CallbackQuery object.
    - callback_data: The callback data.
    - state: The FSMContext object.
    - bot: The Bot instance.
    - action_mapping: A dictionary mapping callback actions to answers.
    """
    data = await state.get_data()
    position = data.get('position')
    questions = data.get('questions')
    message_id = query.message.message_id
    chat_id = query.message.chat.id

    answer = action_mapping[callback_data.action]
    await state.update_data({f"answer_{position}": answer})

    new_position = position + 1
    new_position = await update_data_telegram_id(state, new_position)

    if new_position >= len(questions):
        await send_results_and_clear(state, bot, chat_id, message_id)
    else:
        await state.update_data(position=new_position)
        new_question_text = questions[new_position]['question']
        question_type = questions[new_position]['type']
        await display_question(chat_id, message_id, new_question_text,
                               question_type, bot)


@question_router.callback_query(
    AnswerCallback.filter(F.action.in_(
        [Action.yes, Action.no, Action.sometimes, Action.further])))
async def answer_handler(query: CallbackQuery, callback_data: AnswerCallback,
                         state: FSMContext, bot: Bot):
    action_mapping = {
        Action.yes: 'Да',
        Action.no: 'Нет',
        Action.sometimes: 'Иногда',
        Action.further: 'Принято'
    }
    await handle_callback_query_action(query, callback_data, state, bot,
                                       action_mapping)


@question_router.callback_query(
    SexCallback.filter(F.action.in_([Sex.male, Sex.female])))
async def sex_handler(query: CallbackQuery, callback_data: SexCallback,
                      state: FSMContext, bot: Bot):
    action_mapping = {
        Sex.male: 'М',
        Sex.female: 'Ж'
    }
    await handle_callback_query_action(query, callback_data, state, bot,
                                       action_mapping)


async def send_results_and_clear(state, bot, chat_id, message_id):
    """
    Send results and clear the state.

    Args:
    - state: The FSMContext object.
    - bot: Bot instance.
    - chat_id: ID of the chat.
    - message_id: ID of the message.
    """
    updated_data = await state.get_data()
    json_data = prepare_answers(updated_data)

    async with HttpClient() as session:
        response = await session.post(f'{settings.HOST}api/submit/', json_data)
        telegram_id = updated_data.get('telegram_id')
        response = await session.get(
            f'{settings.HOST}api/get_result/{telegram_id}/')

    result_data = response
    result = result_data['result']
    result_test = result_data['test']

    if updated_data.get('questions')[-1]['type'] == 'question':
        await bot.delete_message(chat_id=chat_id, message_id=message_id)

    await bot.edit_message_text(chat_id=chat_id,
                                message_id=message_id,
                                text=tests_result(result_test, result))
    await state.clear()


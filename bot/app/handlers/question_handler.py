from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, \
    ReplyKeyboardRemove, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.handlers.test.states import Question

bool_answers = {
    "Да": "true",
    "Нет": "false"
}

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

test_1 = {
    'questions': [
        {
            'questionId': 1,
            'type': 'string',
            'question': "How are you?"
        },
        {
            'questionId': 2,
            'type': 'bool',
            'question': "Are you woman?"
        },
    ]
}

question_router = Router()

@question_router.message(Command("cancel"))
@question_router.message(F.text.casefold() == "отмена")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
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
    test_id = query.data
    await state.update_data(testId=test_id)
    # Тут получаем список вопросов
    position = 0
    questions = test_1['questions']  # Пока берем со словаря
    await state.set_state(Question.answer)
    await state.update_data(questions=questions)
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

    answer = message.text
    if questions[position]['type'] == "bool":
        if validate_bool_answer(answer):
            answer = bool_answers[answer]
        else:
            await message.answer(
                "Пожалуйста воспользуйтесь кнопкой."
            )
            return
    await state.update_data({f"answer_{position}": answer})
    await state.update_data(position=position+1)
    if position+1 > len(questions)-1:
        updated_data = await state.get_data()
        message_text = prepare_json_data(updated_data)
        await state.clear()
        await message.answer(
            message_text,
            reply_markup=ReplyKeyboardRemove(),
            parse_mode="HTML"
        )
    else:
        await message.answer(
            questions[position+1]['question'],
            reply_markup=markup_keyboard(
                questions[position+1]['type']
            )
        )


def inline_builder(tests: list):
    builder = InlineKeyboardBuilder()
    for test in tests:
        builder.button(text=test['name'], callback_data=str(test['id']))
    builder.adjust(1, 1)
    return builder


def markup_keyboard(question_type):
    if question_type == "bool":
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


def validate_bool_answer(answer: str):
    available_answers = ['Да', 'Нет']
    if answer in available_answers:
        return True
    return False


def prepare_json_data(data: dict):
    questions = data.get('questions')
    test_id = data.get('testId')
    message = f"'testId': '{test_id}',\n" \
              f"'answers': [\n"
    for n in range(0, len(questions)):
        message += f"'questionId': {questions[n]['questionId']},\n" \
                   f"'type': {questions[n]['type']},\n" \
                   f"'answer': {data.get(f'answer_{n}')}\n"
    message += "]"
    return message


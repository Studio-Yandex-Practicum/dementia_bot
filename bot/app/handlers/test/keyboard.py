from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.handlers.test.callback import AnswerCallback, Action, SexCallback, Sex


def answer_keyboarder():
    """
    Generates an inline keyboard with 'Yes' and 'No' buttons.

    Returns:
        InlineKeyboardBuilder: An instance of InlineKeyboardBuilder
        with 'Yes' and 'No' buttons.
    """
    builder = InlineKeyboardBuilder()
    builder.button(
        text=Action.yes,
        callback_data=AnswerCallback(action=Action.yes)
    )
    builder.button(
        text=Action.no,
        callback_data=AnswerCallback(action=Action.no)
    )

    return builder.as_markup()


def triple_answer_keyboarder():
    """
    Generates an inline keyboard with 'Yes', 'No', and 'Sometimes' buttons.

    Returns:
        InlineKeyboardBuilder: An instance of InlineKeyboardBuilder
        with 'Yes', 'No', and 'Sometimes' buttons.
    """
    builder = InlineKeyboardBuilder()
    builder.button(
        text=Action.yes,
        callback_data=AnswerCallback(action=Action.yes)
    )
    builder.button(
        text=Action.no,
        callback_data=AnswerCallback(action=Action.no)
    )
    builder.button(
        text=Action.sometimes,
        callback_data=AnswerCallback(action=Action.sometimes)
    )
    return builder.as_markup()


def further_keyboarder():
    """
    Generates an inline keyboard with a 'Further' button.

    Returns:
        InlineKeyboardBuilder: An instance of InlineKeyboardBuilder
        with a 'Further' button.
    """
    builder = InlineKeyboardBuilder()
    builder.button(
        text=Action.further,
        callback_data=AnswerCallback(action=Action.further)
    )
    return builder.as_markup()


def sex_keyboarder():
    """
    Generates an inline keyboard with 'Male' and 'Female' buttons.

    Returns:
        InlineKeyboardBuilder: An instance of InlineKeyboardBuilder
        with 'Male' and 'Female' buttons.
    """
    builder = InlineKeyboardBuilder()
    builder.button(
        text=Sex.male,
        callback_data=SexCallback(action=Sex.male)
    )
    builder.button(
        text=Sex.female,
        callback_data=SexCallback(action=Sex.female)
    )

    return builder.as_markup()


def prepare_answers(data: dict):
    """
    Prepares answers in a dictionary format to be submitted.

    Args:
        data (dict): User data containing answers and question information.

    Returns:
        dict: A dictionary with prepared answers.
    """
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


def inline_builder(tests: list):
    """
    Builds an inline keyboard with buttons for each test.

    Args:
        tests (list): List of tests.

    Returns:
        InlineKeyboardBuilder: An instance of InlineKeyboardBuilder
        with buttons for each test.
    """
    builder = InlineKeyboardBuilder()
    for test in tests:
        builder.button(text=test['title'], callback_data=str(test['id']))
    builder.adjust(2, 1)
    return builder

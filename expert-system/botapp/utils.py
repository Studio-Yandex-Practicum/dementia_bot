from datetime import datetime

from botapp.constants import PERSONAL_DETAILS, OK, DEVIATIONS, DEMENTIA, NOTEND, COUNTRIES
from botapp.models import TestParticipant, UserAnswer


def create_participant(questions, test_id):
    """Создание участника теста."""
    data_dict = {}

    for question in questions:
        type = question['type']

        if type in PERSONAL_DETAILS:
            data_dict[type] = question['answer']

        else:
            data_dict[type] = None

    dob_str = data_dict['birthdate']

    if dob_str:
        age = datetime.now().year - datetime.strptime(dob_str, '%Y-%m-%d').year

    else:
        age = None

    participant = TestParticipant.create_from_data(test_id, age, data_dict)

    return participant


def create_user_answers(participant, questions, test_id):
    """Создание ответов пользователя."""
    total_test_score = 0

    questions_dict = {
                      q['questionId']: q['answer']
                      for q in questions
                      if q['type'] not in PERSONAL_DETAILS
                    }

    user_answers = []

    for question_id, answer_text in questions_dict.items():
        score = 0
        if answer_text.lower() == 'да':
            score = 1
        elif question_id == 14:
            current_date = datetime.now().strftime('%d.%m.%Y').split('.')
            answer_date = answer_text.split('.')
            score = 0
            if current_date[0] == answer_date[0]:
                score += 2
            elif (int(current_date[0]) - 3) <= (int(answer_date[0])) <= (int(current_date[0]) + 3):
                score += 1
            else:
                score += 0
            if current_date[1] == answer_date[1]:
                score += 1
            else:
                score += 0
            if current_date[2] == answer_date[2]:
                score += 1
            else:
                score = 0
        elif question_id == 15:
            right_answer = ['носорог', 'арфа']
            for word in answer_text.lower():
                if word in right_answer:
                    score += 1
                else:
                    score += 0
        elif question_id == 16:
            right_answer = ['цветы', 'цветок', 'растения', 'растение', 'природа/флора']
            if answer_text.lower() in right_answer:
                score = 1
        elif question_id == 17:
            right_answer = ['шесть', '6']
            if answer_text.lower() in right_answer:
                score = 1
        elif question_id == 18:
            right_answer = ['1 рубль 95 копеек', '1,95']
            if answer_text.lower() in right_answer:
                score = 1
        elif question_id == 22:
            country_score = 0
            for country in list(set(answer_text.lower())):
                if country in COUNTRIES:
                    country_score += 1
                else:
                    country_score += 0
            if country_score == 12:
                score = 2
            elif 10 <= country_score <= 11:
                score = 1
            else:
                score = 0

        total_test_score += score

        user_answer = UserAnswer(
            participant=participant,
            question_id=question_id,
            answer=answer_text,
            test_id=test_id,
            score=score
        )
        user_answers.append(user_answer)

    UserAnswer.objects.bulk_create(user_answers)

    participant.total_score = total_test_score
    if total_test_score == 0:
        participant.result = NOTEND
    elif 0 <= total_test_score <= 5:
        participant.result = OK
    elif 6 <= total_test_score <= 14:
        participant.result = DEVIATIONS
    elif total_test_score >= 15:
        participant.result = DEMENTIA

    participant.save()

from datetime import datetime

from botapp.constants import PERSONAL_DETAILS
from botapp.models import TestParticipant, UserAnswer


def create_participant(participant_data, test_id):
    """Создание участника теста."""

    # data_dict = {}

    #for question in questions:
    #    question_type = question['type']
#
    #    if question_type in PERSONAL_DETAILS:
    #        data_dict[question_type] = question['answer']
#
    #    else:
    #        data_dict[question_type] = None
#
    dob_str = participant_data.get('birthdate')

    if dob_str:
        age = datetime.now().year - datetime.strptime(dob_str, '%Y-%m-%d').year

    else:
        age = None

    participant = TestParticipant.create_from_data(test_id, age,
                                                   participant_data)

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
        score = 1 if answer_text.lower() == 'да' else 0
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

    participant.save()

from datetime import datetime

from .models import Question, Test, TestParticipant, UserAnswer


def create_participant(validated_data):
    """Создание участника теста."""

    questions_data = validated_data['questions']
    questions_dict = {q['questionId']: q['answer'] for q in questions_data}

    name = questions_dict[1]
    dob_str = questions_dict[2]
    gender = questions_dict[3]
    profession = questions_dict[4]
    email = questions_dict[5]
    telegram_id = questions_dict[6]
    dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
    current_year = datetime.today().year
    age = current_year - dob.year - ((
                                     datetime.now().month,
                                     datetime.now().day) < (dob.month, dob.day
                                                            ))

    participant = TestParticipant(
        test=Test.objects.get(pk=validated_data['testId']),
        email=email,
        name=name,
        age=age,
        telegram_id=telegram_id,
        profession=profession,
        gender=gender,
    )
    participant.save()

    return participant


def create_user_answers(participant, validated_data):
    """Создание ответов пользователя."""

    total_test_score = 0
    questions_data = validated_data['questions']
    questions_dict = {q['questionId']: q['answer'] for q in questions_data}
    user_answers = []

    questions_in_range = Question.objects.filter(pk__in=range(7, 28))
    questions_map = {q.pk: q for q in questions_in_range}

    user_answers = []

    for question_id in range(7, 28):
        answer_text = questions_dict.get(question_id)
        score = 1 if answer_text.lower() == 'да' else 0
        total_test_score += score

        user_answer = UserAnswer(
            participant=participant,
            question=questions_map[question_id],
            answer=answer_text,
            test=participant.test,
            score=score
        )
        user_answers.append(user_answer)
    UserAnswer.objects.bulk_create(user_answers)
    participant.total_score = total_test_score
    participant.save()

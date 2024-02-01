from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from botapp.constants import (
    RELATIVE_MESSAGE_ONE,
    RELATIVE_MESSAGE_THREE,
    RELATIVE_MESSAGE_TWO,
    SELF_MESSAGE_ONE,
    SELF_MESSAGE_THREE,
    SELF_MESSAGE_TWO,
)
from botapp.models import (
    Answer,
    AnswerRelative,
    DementiaTestCase,
    ResultAnswer,
    ResultAnswerRelative,
    Test,
    TestParticipant,
)
from botapp.serializers import (
    JSONSerializer,
    TestDataSerializer,
    TestReadSerializer,
    TestResultParticipantSerializer,
    TestSerializer,
)
from botapp.services.test_service import TestService, TestServiceRelative
from botapp.utils import create_participant, create_user_answers


@swagger_auto_schema(
    method='GET',
    manual_parameters=[
        openapi.Parameter(
            name='test_id',
            in_=openapi.IN_PATH,
            type=openapi.TYPE_STRING,
            description='Идентификатор теста (набор вопросов)',
            required=True),
        ],
    responses={
            status.HTTP_200_OK: openapi.Response(
                description="Успешный запрос",
                examples={
                    "application/json": {
                        "title": "Test name 1",
                        "questions": [
                            {
                            "questionId": 7,
                            "type": "Question type",
                            "question": "Текст вопроса"
                            },
                            {
                            "questionId": 19,
                            "type": "Question type",
                            "question": "Текст вопроса"
                            }
                        ]
                    }
            }
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="Тест не найден",
            examples={
                "application/json": {
                            "error": "Тест не найден"
                }
            }
        )
    }
)
@api_view(['GET'])
def get_test(request, test_id):
    """Получаем айди теста и возвращаем впоросы к нему"""

    try:
        test = Test.objects.get(id=test_id)
        serializer = TestSerializer(test)
        return Response(serializer.data)

    except Test.DoesNotExist:
        return Response({"error": "Тест не найден"},
                        status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    method='POST',
    request_body=TestDataSerializer,
    responses={
        status.HTTP_201_CREATED: openapi.Response(
            description="Успешный запрос на сохранение результатов теста",
            examples={
                "application/json": {
                    "message": "Тест завершен успешно!"
                    }
                }
            ),
        status.HTTP_400_BAD_REQUEST: openapi.Response(
            description="Некорректные данные в ответах теста",
            )
        }
    )
@api_view(['POST'])
def submit_test(request):
    """Получаем данные от пользователя и сохраняем их в БД."""

    serializer = TestDataSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    validated_data = serializer.validated_data
    test_id = validated_data['testId']
    questions = validated_data['questions']
    participant = create_participant(questions, test_id)
    create_user_answers(participant, questions, test_id)

    return Response({"message": "Тест завершен успешно!"},
                    status=status.HTTP_201_CREATED)


@swagger_auto_schema(
    method='GET',
    responses={
        status.HTTP_200_OK: openapi.Response(description="Успешный запрос",
            examples={
                "application/json": [
                    {
                        "id": 1,
                        "title": "Test name 1"
                    },
                    {
                        "id": 2,
                        "title": "Test name 2"
                    }
                ]
            }
        ),
    }
)
@api_view(['GET'])
def get_all_tests(request):
    """Получаем все доступные тесты."""
    tests = Test.objects.all()
    serializer = TestReadSerializer(tests, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='POST',
    request_body=JSONSerializer,
    responses={
        status.HTTP_200_OK: openapi.Response(
        description="Отчет по результатам теста успешно сформирован",
            examples={
                "application/json": 
                    "text message"
                }
            ),
        status.HTTP_400_BAD_REQUEST: openapi.Response(
            description="Некорректные данные в ответах теста",
        )
    }
)
@api_view(['POST'])
def submit_result(request):
    """Получаем JSON с ответами и отправляем результат в бота"""
    serializer = JSONSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(status=status.HTTP_400_BAD_REQUEST)

    question_list = request.data['questions']
    self_result = sum([i['score'] for i in question_list[0:26]])
    # relative_result = sum([i['score'] for i in question_list[27:53]])

    message = ''
    if self_result <= 14:
        message = SELF_MESSAGE_THREE
    elif 15 <= self_result <= 16:
        message = SELF_MESSAGE_TWO
    elif 17 <= self_result <= 22:
        message = SELF_MESSAGE_ONE

    return Response(message, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='GET',
    manual_parameters=[
        openapi.Parameter(
            name='telegram_id',
            in_=openapi.IN_PATH,
            type=openapi.TYPE_STRING,
            description=('Telegram-идентификатор пользователя,'
                          ' проходящего тестирование'),
            required=True),
        ],
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="Успешный запрос",
            examples={
                "application/json": {
                    "name": "Some user_name",
                    "test": 1,
                    "total_score": 3,
                    "result": "Test result"}
                }
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="Участник не найден",
            examples={
                "application/json": {
                            "error": "Указанный участник не найден"
                }
            }
        )
    }
)
@api_view(['GET'])
def get_result(request, telegram_id):
    """
    Получаем JSON с результатами прохождения теста
    участника с указанным telegram_id.
    """
    try:
        result = TestParticipant.objects.get(telegram_id=telegram_id)
        serializer = TestResultParticipantSerializer(result)
        return Response(serializer.data)
    except TestParticipant.DoesNotExist:
        return Response({"error": "Указанный участник не найден"},
                        status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_result_new(test_case_id: int, forClosePerson: bool) -> int:
    result = 0
    test_case = DementiaTestCase.objects.get(id=test_case_id)

    for answer in Answer.objects.filter(test_case=test_case_id):
        if forClosePerson:
            f = getattr(TestServiceRelative, "question_" + str(answer.question))
            try:
                score = f(answer.answer_value, answer.image)
            except Exception:
                score = 0
            question_id = AnswerRelative.objects.get(test_case=answer.test_case, question=answer.question)
            ResultAnswerRelative.objects.update_or_create(question_id=question_id, defaults={"answer_value": score})
        else:
            f = getattr(TestService, "question_" + str(answer.question))
            try:
                score = f(answer.answer_value, answer.image)
            except Exception:
                score = 0
            question_id = Answer.objects.get(test_case=answer.test_case, question=answer.question)
            ResultAnswer.objects.update_or_create(question_id=question_id, defaults={"answer_value": score})

        result += score
    return result

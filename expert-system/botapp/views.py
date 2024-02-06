from botapp.models import Test, TestParticipant
from botapp.serializers import (TestDataSerializer, TestReadSerializer,
                                TestSerializer, JSONSerializer,
                                TestResultParticipantSerializer,
                                AnswerImageSerializer)
from botapp.utils import create_participant, create_user_answers, image_detected
from botapp.constants import (SELF_MESSAGE_ONE, SELF_MESSAGE_TWO,SELF_MESSAGE_THREE,
                        RELATIVE_MESSAGE_ONE, RELATIVE_MESSAGE_TWO, RELATIVE_MESSAGE_THREE)
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import io
from PIL import Image


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


@api_view(['POST'])
def test_image(request, test_id, session_id):
    """Получаем ответ с изображением, распознаем и сохраняем"""

    data = request.data
    data['test_id'] = test_id
    data['session_id'] = session_id

    serializer = AnswerImageSerializer(data=data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    validated_data = serializer.validated_data
    image_answer = validated_data['file']

    question_id = request.headers['Question']
    validated_data['question_id'] = question_id

    file_extention = image_answer.name.split(".")[-1]
    new_filename = f'tid{test_id}_sid{session_id}_qid{question_id}.'
    image_answer.name = new_filename + file_extention
    fs = FileSystemStorage(location=settings.MEDIA_ROOT)
    if fs.exists(image_answer.name):
        fs.delete(image_answer.name)
    fs.save(image_answer.name, image_answer)

    img = f'{settings.MEDIA_ROOT}/{image_answer.name}'
    score = image_detected(img)
    validated_data['score'] = score

    return Response(serializer.data, status=status.HTTP_200_OK)
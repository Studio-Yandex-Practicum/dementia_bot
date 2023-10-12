from botapp.models import Test
from botapp.serializers import (TestDataSerializer, TestReadSerializer,
                                TestSerializer, JSONSerializer)
from botapp.utils import create_participant, create_user_answers
from botapp.constants import (SELF_MESSAGE_ONE, SELF_MESSAGE_TWO,SELF_MESSAGE_THREE,
                        RELATIVE_MESSAGE_ONE, RELATIVE_MESSAGE_TWO, RELATIVE_MESSAGE_THREE)
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


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


@api_view(['GET'])
def get_all_tests(request):
    """Получаем все доступные тесты."""
    tests = Test.objects.all()
    serializer = TestReadSerializer(tests, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


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

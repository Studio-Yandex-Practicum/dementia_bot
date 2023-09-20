from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Test
from .serializers import TestDataSerializer, TestSerializer
from .utils import create_participant, create_user_answers


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
    participant = create_participant(validated_data)
    create_user_answers(participant, validated_data)

    return Response({"message": "Тест завершен успешно!"},
                    status=status.HTTP_201_CREATED)

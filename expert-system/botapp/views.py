from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Test
from .serializers import TestSerializer
from rest_framework import status


@api_view(['GET'])
def get_test(request, test_id):
    """Получаем айди теста и возвращаем впоросы к нему"""

    try:
        test = Test.objects.get(id=test_id)
        serializer = TestSerializer(test)
        return Response(serializer.data)

    except Test.DoesNotExist:
        return Response({"error": "Test not found"},
                        status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def submit_test(request):
    pass

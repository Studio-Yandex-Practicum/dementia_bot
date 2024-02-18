from botapp.serializers import AnswerImageSerializer
from botapp.utils import image_detected_8, image_detected_7, now_date
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from PIL import Image
from io import BytesIO


@api_view(['POST'])
def answer_watch(request):
    """Получаем ответ (N8) с изображением, распознаем и сохраняем."""

    serializer = AnswerImageSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    validated_data = serializer.validated_data

    image_answer = validated_data['file']
    

    file_extention = image_answer.name.split(".")[-1]
    new_filename = f'watch_{now_date()}_sc{"3"}.'
    image_answer.name = new_filename + file_extention
    fs = FileSystemStorage(location=settings.MEDIA_ROOT)
    fs.save(image_answer.name, image_answer)
    score = image_detected_8(f"media/{image_answer}")

    validated_data['answer_score'] = score

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def answer_copy_test(request):
    """Получаем ответ (N7) с изображением, распознаем и сохраняем."""

    serializer = AnswerImageSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    validated_data = serializer.validated_data

    image_answer = validated_data['file']
    image = Image.open(BytesIO(image_answer.read()))
    score = image_detected_7(image)

    file_extention = image_answer.name.split(".")[-1]
    new_filename = f'copy_{now_date()}_sc{score}.'
    image_answer.name = new_filename + file_extention
    fs = FileSystemStorage(location=settings.MEDIA_ROOT)
    fs.save(image_answer.name, image_answer)

    validated_data['answer_score'] = score

    return Response(serializer.data, status=status.HTTP_200_OK)

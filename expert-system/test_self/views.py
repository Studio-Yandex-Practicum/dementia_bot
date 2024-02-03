from test_self.models import Answer, Session
from test_self.serializers import AnswerTextSerializer, AnswerImageSerializer, SessionSerializer, ResultSerializer
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser


@api_view(['POST'])
def submit_text_answer(request, test_id, session_id):
    """Получаем ответ и сохраняем в БД."""

    serializer = AnswerTextSerializer(data=request.data)

    if not serializer.is_valid():
        return Response("Wrong answer format", status=status.HTTP_400_BAD_REQUEST)

    validated_data = serializer.validated_data

    text_answer = validated_data['text_answer']
    question_id = validated_data['question_id']

    answer = Answer(
            test_id=test_id,
            session_id=session_id,
            question_id=question_id,
            text_answer=text_answer
        )
    answer.save()

    return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
@parser_classes([MultiPartParser])
def submit_image_answer(request, test_id, session_id):
    """Получаем ответ с изображением и сохраняем в БД."""

    serializer = AnswerImageSerializer(data=request.data)
    if not serializer.is_valid():
        return Response("Wrong answer format", status=status.HTTP_400_BAD_REQUEST)

    validated_data = serializer.validated_data
    image_answer = validated_data['image_answer']

    question_id = request.headers['Question']

    file_extention = image_answer.name.split(".")[-1]
    new_filename = f'tid{test_id}_sid{session_id}_q{question_id}.'
    image_answer.name = new_filename + file_extention

    answer = Answer(
            test_id=test_id,
            session_id=session_id,
            question_id=question_id,
            image_answer=image_answer
        )
    answer.save()

    return Response(status=status.HTTP_201_CREATED)


@api_view(['POST'])
def submit_session(request, test_id):
    """Создание и передача id сессии."""

    session = Session.objects.create()
    serializer = SessionSerializer(session)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


# Этот запрос будет использовать механизм оценки вопросов, который
# подготовил Владимир
@api_view(['GET'])
def get_result(request, test_id, session_id):
    """Оценка ответов и подсчет суммарного балла."""
    pass

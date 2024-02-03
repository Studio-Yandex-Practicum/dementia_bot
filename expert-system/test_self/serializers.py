from test_self.models import Answer, Session
from rest_framework import serializers


class AnswerTextSerializer(serializers.ModelSerializer):
    """Сериализатор для текстовых ответов."""

    question = serializers.IntegerField(source='question_id')
    answer = serializers.CharField(source='text_answer')

    class Meta:
        model = Answer
        fields = ('answer', 'question')


class AnswerImageSerializer(serializers.ModelSerializer):
    """Сериализатор для графических ответов."""

    multipart_file = serializers.ImageField(
        source='image_answer')

    class Meta:
        multipart = True
        model = Answer
        fields = ('multipart_file',)


class SessionSerializer(serializers.ModelSerializer):
    """Сериализатор для сессий."""

    session_id = serializers.IntegerField(
        source='id', read_only=True)

    class Meta:
        model = Session
        fields = ('session_id',)


class ResultSerializer(serializers.ModelSerializer):
    """Сериализатор для результата тестирования."""

    result = serializers.methodField(read_only=True)

    # class Meta:
    #     model = Session
    #     fields = ('session_id',)
    
from rest_framework import serializers
from .models import Test, Question


class QuestionSerializer(serializers.ModelSerializer):
    """Сериализатор для вопросов. Переопределил поля как в задании."""

    questionId = serializers.IntegerField(source='id')
    type = serializers.CharField(source='question_type')
    question = serializers.CharField(source='text')

    class Meta:
        model = Question
        fields = ('questionId', 'type', 'question')


class TestSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Test
        fields = ('title', 'questions')

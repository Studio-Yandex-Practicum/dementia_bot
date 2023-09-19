from rest_framework import serializers
from .models import Test, Question
from .validators import validate_email, validate_dob


class QuestionSerializer(serializers.ModelSerializer):
    """Сериализатор для отдачи вопросов. Переопределил поля как в задании."""
    
    questionId = serializers.IntegerField(source='id')
    type = serializers.CharField(source='question_type')
    question = serializers.CharField(source='text')
        
    class Meta:
        model = Question
        fields = ('questionId', 'type', 'question') 


class TestSerializer(serializers.ModelSerializer):
    """Сериализатор для теста."""

    questions = QuestionSerializer(many=True)

    class Meta:
        model = Test
        fields = ('title', 'questions')


class QuestionWithAnswerSerializer(serializers.Serializer):
    """Сериализатор для обработки вопросов с ответами."""

    questionId = serializers.IntegerField()
    type = serializers.CharField()
    answer = serializers.CharField()

    class Meta:
        fields = ('questionId', 'type', 'answer')


class TestDataSerializer(serializers.Serializer):
    """Сериализатор для обработки данных от пользователя."""

    testId = serializers.IntegerField()
    questions = QuestionWithAnswerSerializer(many=True)

    def validate(self, data):
        questions = {question['questionId']: question for question in data['questions']}
        
        email = questions[5]['answer']
        validate_email(email)
        
        dob = questions[2]['answer']
        validate_dob(dob)
        
        return data

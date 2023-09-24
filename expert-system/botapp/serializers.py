from rest_framework import serializers

from botapp.models import Question, Test
from botapp.validators import validate_dob, validate_email


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
        self.validate_data_integrity(data)
        self.validate_birthdate(data)
        self.validate_email(data)
        return data

    def validate_data_integrity(self, data):
        """Проверяем, что данные от пользователя валидны."""

        questions = data.get('questions', [])

        for question in questions:
            if not all(
                question.get(key)
                for key in ('questionId', 'type', 'answer')
            ):
                raise serializers.ValidationError('Неверный формат данных')

    def validate_birthdate(self, data):
        """Проверяем, что дата рождения валидна."""

        self.validate_question_type(data, 'birthdate', validate_dob)

    def validate_email(self, data):
        """Проверяем, что email валиден."""

        self.validate_question_type(data, 'email', validate_email)

    def validate_question_type(self, data, target_type, validation_function):
        questions = data.get('questions', [])

        for question in questions:
            question_type = question.get('type')
            answer = question.get('answer')

            if question_type == target_type:
                validation_function(answer)


class TestReadSerializer(serializers.ModelSerializer):
    """Сериализатор для отдачи тестов."""

    class Meta:
        model = Test
        fields = ('id', 'title',)

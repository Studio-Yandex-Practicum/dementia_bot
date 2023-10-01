from django.shortcuts import get_object_or_404
from rest_framework import serializers

from botapp.constants import OPTION_CHOICES
from botapp.models import Question, QuestionImage, Test
from botapp.validators import validate_dob, validate_email

OPTION_CHOICES_DICT = dict(OPTION_CHOICES)


class OptionSerializer(serializers.Serializer):
    """Сериализатор для вариантов ответов."""

    text = serializers.CharField()
    requiresExplanation = serializers.BooleanField(
        source='requires_explanation'
    )

    class Meta:
        fields = ('text', 'requiresExplanation')


class QuestionImageSerializer(serializers.Serializer):
    """Сериализатор для изображений вопросов."""

    class Meta:
        model = QuestionImage
        fields = ('image',)


class QuestionSerializer(serializers.ModelSerializer):
    """Сериализатор для отдачи вопросов теста."""

    questionId = serializers.IntegerField(source='id')
    type = serializers.CharField(source='question_type')
    question = serializers.CharField(source='text')
    count = serializers.IntegerField()
    options = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ('questionId', 'type', 'question',
                  'count', 'options', 'image_url')

    def to_representation(self, instance):
        """Переопределяем метод to_representation и убираем пустые поля в ответе.
           В принципе, их можно оставить. Тогда просто удаляем метод целиком.
           Протестировано, все работает при удалении.
        """

        representation = super().to_representation(instance)

        if not representation['options']:
            representation.pop('options')
        if representation['count'] == 1:
            representation.pop('count')
        if not representation['image_url']:
            representation.pop('image_url')
        return representation

    def get_options(self, obj):
        """Возвращает список вариантов ответов для данного вопроса."""

        options_list = []

        for option in obj.options.all():
            translated_text = OPTION_CHOICES_DICT.get(option.text, option.text)

            # Если опция требует объяснения, добавляем поле requiresExplanation
            if option.requires_explanation:
                options_list.append(
                    {"text": translated_text,
                     "requiresExplanation": option.requires_explanation}
                    )
            else:
                options_list.append(translated_text)

        return options_list

    def get_image_url(self, obj):
        """Возвращает список урлов изображений для данного вопроса."""

        return [img.image.url for img in obj.images.all()]


class TestSerializer(serializers.ModelSerializer):
    """Сериализатор для теста."""

    questions = QuestionSerializer(many=True)

    class Meta:
        model = Test
        fields = ('questions', )


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
        self.validate_question_count(data)
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

    def validate_question_count(self, data):
        """
        Проверяем, что количество ответов соответствует
        количеству вопросов в тесте.
        """

        test_id = data.get('testId')
        questions_count_in_request = len(data.get('questions', []))

        test = get_object_or_404(Test.objects.all(), id=test_id)
        questions_count_in_test = test.questions.count()

        if questions_count_in_request != questions_count_in_test:
            error_msg = (
                        f'Ожидалось {questions_count_in_test} ответов, '
                        f'но получено {questions_count_in_request}'
                        )
            raise serializers.ValidationError(error_msg)

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

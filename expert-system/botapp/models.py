import botapp.constants as const
from django.db import models
from django.utils.html import format_html


class Test(models.Model):
    """Тесты для пользователей."""

    title = models.CharField(max_length=255, verbose_name="Название теста")
    description = models.TextField(blank=True, verbose_name="Описание теста")
    questions = models.ManyToManyField(
                    'Question',
                    related_name='tests',
                    verbose_name="Вопросы в тесте",
                    blank=True
                    )

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"

    def __str__(self):
        return self.title


class Question(models.Model):
    """
    Вопросы для тестов. Есть возможность выбрать тип вопроса.
    Подразумевается, что баллы за ответы на вопросы да/нет фиксированные.
    Если нет, то надо менять модель.
    """

    text = models.TextField(verbose_name="Текст вопроса")
    count = models.PositiveIntegerField(
                    default=1, verbose_name="Ожидаемое количество ответов"
                    )
    question_type = models.CharField(max_length=50,
                                     choices=const.QUESTION_TYPES,
                                     default='text',
                                     verbose_name="Тип вопроса")

    def __str__(self):
        return self.text[:50]

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


class QuestionImage(models.Model):
    """Изображения для вопросов."""
    question = models.ForeignKey(Question, related_name='images',
                                 on_delete=models.CASCADE)
    image = models.ImageField(upload_to='questions_images/',
                              verbose_name="Изображение")

    def image_tag(self):
        """Отображение изображения в админке."""

        return format_html('<img src="{}" width="50" height="50" />',
                           self.image.url)

    image_tag.short_description = 'Изображение'
    image_tag.allow_tags = True


class Option(models.Model):
    question = models.ForeignKey(Question, related_name='options',
                                 on_delete=models.CASCADE)
    text = models.CharField(max_length=50, choices=const.OPTION_CHOICES,
                            verbose_name="Текст варианта ответа")
    requires_explanation = models.BooleanField(
                            default=False, verbose_name="Требует пояснение?"
                            )

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Вариант ответа"
        verbose_name_plural = "Варианты ответов"


class UserAnswer(models.Model):
    """
    Ответы пользователей на вопросы.
    Подразумевается, что баллы за ответы на вопросы да/нет фиксированные.
    """

    participant = models.ForeignKey('TestParticipant',
                                    on_delete=models.CASCADE,
                                    verbose_name="участник теста")
    question = models.ForeignKey(Question, on_delete=models.CASCADE,
                                 verbose_name="Вопрос")
    answer = models.TextField(blank=True, null=True,
                              verbose_name="Ответ")
    test = models.ForeignKey(Test, on_delete=models.CASCADE,
                             verbose_name="Тест")
    timestamp = models.DateTimeField(auto_now_add=True,
                                     verbose_name="Время прохождения")
    score = models.IntegerField(default=0, verbose_name="Балл")

    def __str__(self):
        return f"{self.participant.name} - {self.score}"

    class Meta:
        verbose_name = "Ответ пользователя"
        verbose_name_plural = "Ответы пользователей"


class TestParticipant(models.Model):
    """Пользователи, которые прошли тест."""

    test = models.ForeignKey(Test, on_delete=models.CASCADE,
                             verbose_name="Тест")
    email = models.EmailField(max_length=255,
                              verbose_name="Email")
    name = models.CharField(max_length=255, verbose_name="Имя")
    age = models.IntegerField(verbose_name="Возраст")
    telegram_id = models.CharField(max_length=255,
                                   verbose_name="ID Telegram")
    gender = models.CharField(max_length=1,
                              choices=const.GENDER_CHOICES,
                              verbose_name="Пол")
    profession = models.CharField(max_length=255, verbose_name="Профессия")
    timestamp = models.DateTimeField(auto_now_add=True,
                                     verbose_name="Время прохождения")
    total_score = models.IntegerField(default=0, verbose_name="Общий балл")

    class Meta:
        verbose_name = "Участник теста"
        verbose_name_plural = "Участники тестов"

    def __str__(self):
        return f"{self.name} - {self.total_score}"

    @classmethod
    def create_from_data(cls, test_id, age, data_dict):
        """Создание участника теста."""

        participant = cls(
            test_id=test_id,
            email=data_dict['email'],
            name=data_dict['name'],
            age=age,
            telegram_id=data_dict['telegram_id'],
            profession=data_dict['occupation'],
            gender=data_dict['gender'],
        )
        participant.save()

        return participant

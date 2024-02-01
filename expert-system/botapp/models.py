from core.mixins import DateMixin
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

import botapp.constants as const


class Test(models.Model):
    """Тесты для пользователей."""

    title = models.CharField(max_length=255, verbose_name="Название теста")
    description = models.TextField(blank=True, verbose_name="Описание теста")
    questions = models.ManyToManyField('Question',
                                       related_name='tests',
                                       verbose_name="Вопросы в тесте",
                                       blank=True)

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

    question = models.TextField(verbose_name="Текст вопроса")
    questionId = models.IntegerField(
        primary_key=True,
        verbose_name="Номер вопроса"
        )
    score = models.IntegerField(verbose_name="Максимальная оценка",
                                null = True)
    type = models.CharField(max_length=50,
                            choices=const.QUESTION_TYPES,
                            default='text',
                            verbose_name="Тип вопроса")

    def __str__(self):
        return self.question[:50]

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


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
    result = models.CharField(
        max_length=255,
        choices=const.RESULT_CHOISES,
        verbose_name="Результат прохождения теста",
        default=const.NOTEND
    )

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


class DementiaTestCase(DateMixin):
    updated_at = None

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Прохождение теста"
        verbose_name_plural = "Прохождения тестов"

    def __str__(self):
        return f"Тест №{self.pk}, {timezone.localtime(self.created_at).strftime('%d.%m.%Y %H:%M')}"


class DemeniaTestCaseAlt(DementiaTestCase):
    class Meta:
        proxy = True
        verbose_name = "Прохождение теста (альт.)"
        verbose_name_plural = "Прохождения тестов (альт.)"


class Answer(DateMixin):
    updated_at = None

    question = models.PositiveSmallIntegerField(
        "Номер вопроса", validators=[MinValueValidator(1), MaxValueValidator(25)]
    )
    answer_value = models.CharField("Значение ответа", max_length=255, null=True)
    test_case = models.ForeignKey(
        DementiaTestCase, on_delete=models.CASCADE, related_name="answers", verbose_name="Прохождение теста"
    )
    image = models.ImageField(upload_to="answer/", verbose_name="Изображение", null=True)

    class Meta:
        unique_together = ("test_case", "question")
        ordering = ["question"]
        verbose_name = "Ответ на вопрос"
        verbose_name_plural = "Ответы на вопросы"


class ResultAnswer(models.Model):
    question_id = models.ForeignKey(
        Answer, on_delete=models.CASCADE, related_name="answer_id", verbose_name="id теста"
    )
    answer_value = models.IntegerField("Количество баллов", blank=True, default="")

    class Meta:
        verbose_name = "Количество баллов за вопрос"
        verbose_name_plural = "Количество баллов за вопросы"


class AnswerRelative(DateMixin):
    updated_at = None

    question = models.PositiveSmallIntegerField(
        "Номер вопроса", validators=[MinValueValidator(1), MaxValueValidator(25)]
    )
    answer_value = models.CharField("Значение ответа", max_length=255, null=True)
    test_case = models.ForeignKey(
        DementiaTestCase, on_delete=models.CASCADE, related_name="answers", verbose_name="Прохождение теста"
    )

    class Meta:
        unique_together = ("test_case", "question")
        ordering = ["question"]
        verbose_name = "Ответ на вопрос"
        verbose_name_plural = "Ответы на вопросы"


class ResultAnswerRelative(models.Model):
    question_id = models.ForeignKey(
        Answer, on_delete=models.CASCADE, related_name="answer_id", verbose_name="id теста"
    )
    answer_value = models.IntegerField("Количество баллов", blank=True, default="")

    class Meta:
        verbose_name = "Количество баллов за вопрос"
        verbose_name_plural = "Количество баллов за вопросы"

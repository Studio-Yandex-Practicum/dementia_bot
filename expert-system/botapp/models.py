from django.db import models

from . import constants as const


class Test(models.Model):
    """Тесты для пользователей."""

    title = models.CharField(max_length=255, verbose_name="Название теста")
    description = models.TextField(blank=True, verbose_name="Описание теста")
    questions = models.ManyToManyField('Question', related_name='tests',
                                       verbose_name="Вопросы в тесте")

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
    question_type = models.CharField(max_length=50,
                                     choices=const.QUESTION_TYPES,
                                     default=const.TEXT,
                                     verbose_name="Тип вопроса")

    def __str__(self):
        return self.text[:50]

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
        return f"{self.user.name} - {self.score}"

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
    total_score = models.IntegerField(default=0, verbose_name="Общий балл")

    class Meta:
        verbose_name = "Участник теста"
        verbose_name_plural = "Участники тестов"

    def __str__(self):
        return f"{self.name} - {self.total_score}"

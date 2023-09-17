from django.contrib.auth.models import User
from django.db import models

TEXT = 'Text Input'
MULTIPLE_CHOICE = 'Yes or no'
PERSONAL = 'Personal question'


QUESTION_TYPES = [
        (TEXT, 'Текст. Ввод информации'),
        (MULTIPLE_CHOICE, 'Выбор да/нет'),
        (PERSONAL, 'Персональные данные'),
    ]


GENDER_CHOICES = (
        ('M', 'Мужчина'),
        ('F', 'Женщина'),
        )


class Test(models.Model):
    """Тесты для пользователей."""

    title = models.CharField(max_length=255, verbose_name="Название теста")
    description = models.TextField(blank=True, verbose_name="Описание теста")
    questions = models.ManyToManyField('Question', related_name='tests',
                                       verbose_name="Вопросы в тесте")

    def calculate_test_score(self, user):
        """Подсчет баллов теста. Набросок"""

        test_score = 0
        test_score = sum(answer.score for answer in UserAnswer.objects.filter(
                         user=user, test=self))

        return test_score

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
    question_type = models.CharField(max_length=50, choices=QUESTION_TYPES,
                                     default=TEXT, verbose_name="Тип вопроса")

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

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name="Пользователь")
    question = models.ForeignKey(Question, on_delete=models.CASCADE,
                                 verbose_name="Вопрос")
    answer = models.TextField(blank=True, null=True,
                              verbose_name="Ответ")
    test = models.ForeignKey(Test, on_delete=models.CASCADE,
                             verbose_name="Тест")
    timestamp = models.DateTimeField(auto_now_add=True,
                                     verbose_name="Время прохождения")
    score = models.IntegerField(default=0, verbose_name="Общий балл")

    def calculate_user_score(self, user):
        """Подсчет баллов пользователя.Набросок"""

        if self.question.question_type == MULTIPLE_CHOICE:
            if self.answer == 'Да':
                self.score = 1
            else:
                self.score = 0
        self.save()

    def __str__(self):
        return f"{self.user.name} - {self.score}"

    class Meta:
        verbose_name = "Ответ пользователя"
        verbose_name_plural = "Ответы пользователей"

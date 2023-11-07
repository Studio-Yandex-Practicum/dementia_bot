import botapp.constants as const
from django.db import models


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
                                null=True)
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
    profession = models.CharField(max_length=255,
                                  verbose_name="Профессия",
                                  default='Нет данных')
    timestamp = models.DateTimeField(auto_now_add=True,
                                     verbose_name="Время прохождения")
    total_score = models.IntegerField(default=0, verbose_name="Общий балл")
    result = models.CharField(max_length=255,
                              choices=const.RESULT_CHOISES,
                              verbose_name="Результат прохождения теста",
                              default=const.NOTEND
    )

    class Meta:
        verbose_name = "Участник теста"
        verbose_name_plural = "Участники тестов"
        get_latest_by = ('telegram_id', 'timestamp')

    def __str__(self):
        return f"{self.name} - {self.total_score}"

    @classmethod
    def create_from_data(cls, test_id, age, data_dict):
        """Создание участника теста."""
        if 'occupation' in data_dict:
            prof = data_dict['occupation']
        else:
            prof = const.NODATA

        participant = cls(
            test_id=test_id,
            email=data_dict['email'],
            name=data_dict['name'],
            age=age,
            telegram_id=data_dict['telegram_id'],
            profession=prof,
            gender=data_dict['gender'],
        )
        participant.save()

        return participant

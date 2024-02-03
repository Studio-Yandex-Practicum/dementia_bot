from django.db import models


class Session(models.Model):
    """Ответы пользователей на вопросы теста."""

    time_stamp = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата/время открытия сессии"
    )

    class Meta:
        verbose_name = "Сессия"
        verbose_name_plural = "Сессии"


class Answer(models.Model):
    """Ответы пользователей на вопросы теста."""

    test_id = models.PositiveSmallIntegerField(
        verbose_name="ID теста",
        null=False
    )
    session_id = models.PositiveSmallIntegerField(
        verbose_name="ID сессии",
        null=False
    )
    question_id = models.PositiveSmallIntegerField(
        verbose_name="ID вопроса",
        null=False
    )
    text_answer = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Текстовый ответ на вопрос"
    )
    image_answer = models.ImageField(
        upload_to="image_answer/",
        verbose_name="Графический ответ на вопрос",
        null=True,
        blank=True
    )
    ranking = models.PositiveSmallIntegerField(
        verbose_name="Оценка ответа в баллах",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"
        constraints = [
            models.UniqueConstraint(
                fields=['session_id', 'question_id'],
                name='unique_pair_session-question'
            )
        ]
    
    def __str__(self):
        return f"Сессия {self.session_id} - вопрос {self.question_id}"
from django.db import models


class DateMixin(models.Model):
    """Миксин добавления дат.

    Attributes:
        created_at: Дата создания
        updated_at: Дата обновления
    """

    created_at = models.DateTimeField("Дата создания", auto_now_add=True, help_text="Заполняется автоматически")
    updated_at = models.DateTimeField("Дата обновления", auto_now=True, help_text="Заполняется автоматически")

    class Meta:
        abstract = True
        ordering = ["-updated_at"]

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


TEXT = 'Text Input'
MULTIPLE_CHOICE = 'Yes or no'
PERSONAL = 'Personal question'


QUESTION_TYPES = [
        (TEXT, 'Текст. Ввод информации'),
        (MULTIPLE_CHOICE , 'Выбор да/нет'),
        (PERSONAL, 'Персональные данные'),
        
    ]


GENDER_CHOICES = (
        ('M', 'Мужчина'),
        ('F', 'Женщина'),
        )


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


class Test(models.Model):
    """Тесты для пользователей."""

    title = models.CharField(max_length=255, verbose_name="Название теста")
    description = models.TextField(blank=True, verbose_name="Описание теста")
    questions = models.ManyToManyField(Question, related_name='tests',
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

class CustomUserManager(BaseUserManager):
    """Менеджер для создания пользователей."""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен!')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        if password:
            user.set_password(password)  # Установка пароля, если он предоставлен
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        # Создаем суперпользователя, передавая только email и password
        return self.create_user(email, password=password, **extra_fields) 


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Модель пользователя. Дополнительные поля взяты с тестов.
       Прописаны значения по умолчанию, чтобы у нас не сломалось
      создание суперпользователя."""
    
    email = models.EmailField(unique=True, db_index=True)
    name = models.CharField(max_length=255)
    telegram_id = models.IntegerField(blank=True, null=True, db_index=True) 
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    education = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    

    objects = CustomUserManager()

    def __str__(self):
        return self.email



#  Возможно имеет смысл ввести модель для фиксации всех прохождений тестов пользователем.
#       В этом случае надо сделать внешний ключ в UserAnswer и связать их."""

# class UserTestAttempt(models.Model):
#     """Возможно имеет смысл ввести модель для фиксации всех прохождений тестов пользователем.
#       В этом случае надо сделать внешний ключ в UserAnswer и свзать."""

#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     test = models.ForeignKey(Test, on_delete=models.CASCADE)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         verbose_name = "Попытка пользователя"
#         verbose_name_plural = "Попытки пользователей"

    # def __str__(self):
    #     return f"{self.user.name} - {self.test.title} - {self.timestamp}"   


class UserAnswer(models.Model):
    """
    Ответы пользователей на вопросы.
    
    """

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
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


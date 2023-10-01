from django.contrib import admin

from botapp.models import (Option, Question, QuestionImage, Test,
                           TestParticipant, UserAnswer)


@admin.register(UserAnswer)
class TestResultAdmin(admin.ModelAdmin):
    """Ответы пользователей на вопросы."""

    list_display = ('participant', 'test',
                    'question', 'answer',
                    'timestamp', 'score')


@admin.register(TestParticipant)
class UserTestProfileAdmin(admin.ModelAdmin):
    """Профиль участника теста."""

    list_display = ('timestamp', 'name', 'telegram_id',
                    'email', 'age', 'test',
                    'gender', 'profession',
                    'total_score')


class OptionInline(admin.TabularInline):
    """Инлайн для вариантов ответов."""

    model = Option
    extra = 1


class ImageInline(admin.TabularInline):
    """Инлайн для изображений вопросов."""

    model = QuestionImage
    extra = 0
    fields = ('image', 'image_display')
    readonly_fields = ('image_display',)

    def image_display(self, obj):
        return obj.image_tag()
    image_display.short_description = 'Изображение'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Вопросы тестов. Используем инлайны опций и изображений."""

    list_display = ('id', 'text', 'question_type',
                    'test_included', 'answer_options')
    inlines = [OptionInline, ImageInline]

    def answer_options(self, obj):
        """Возвращает список всех вариантов ответов для данного вопроса."""

        return ", ".join(
                [option.get_text_display() for option in obj.options.all()]
                )
    answer_options.short_description = 'Варианты ответов'

    def test_included(self, obj):
        """Возвращает список тестов, в которые включен вопрос."""

        return ", ".join([str(test.title) for test in obj.tests.all()])
    test_included.short_description = 'Тесты, в которые включен вопрос'


class TestQuestionInline(admin.TabularInline):
    """Инлайн для вопросов теста."""

    model = Test.questions.through
    extra = 1


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    """Тесты. Используем инлайн для вопросов."""

    list_display = ('id', 'title', 'description', 'qtty_in_test')
    inlines = [TestQuestionInline]
    exclude = ('questions',)

    def qtty_in_test(self, obj):
        """Возвращает количество вопросов в тесте."""

        return obj.questions.count()

    qtty_in_test.short_description = 'Количество вопросов в тесте'

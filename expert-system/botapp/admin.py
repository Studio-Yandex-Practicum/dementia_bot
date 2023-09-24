from botapp.models import (Question,
                           Test,
                           TestParticipant,
                           UserAnswer,
                           TestQuestion
                           )
from django.contrib import admin


@admin.register(UserAnswer)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('participant', 'test',
                    'question', 'answer',
                    'timestamp', 'score')


@admin.register(TestParticipant)
class UserTestProfileAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'name', 'telegram_id',
                    'email', 'age', 'test',
                    'gender', 'profession',
                    'total_score')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'question_type', 'test_included')

    def test_included(self, obj):
        """Возвращает список тестов, в которые включен вопрос."""

        return ", ".join([str(test.title) for test in obj.tests.all()])
    test_included.short_description = 'Тесты, в которые включен вопрос'


class TestQuestionInline(admin.TabularInline):
    model = TestQuestion
    extra = 1


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'qtty_in_test')
    inlines = [TestQuestionInline]

    def qtty_in_test(self, obj):
        """Возвращает количество вопросов в тесте."""

        return obj.questions.count()

    qtty_in_test.short_description = 'Количество вопросов в тесте'


@admin.register(TestQuestion)
class TestQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'test', 'question')
    list_filter = ('test__title', 'question__question_type')

from django.contrib import admin

from .models import Question, Test, UserAnswer


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    """Не стал включать вопросы в админку, их много.
       Но можно сделать, если надо.
    """
    list_display = ('title', 'description')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'question_type')


@admin.register(UserAnswer)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'question', 'answer', 'timestamp', 'score')
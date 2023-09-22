from botapp.models import Question, Test, TestParticipant, UserAnswer
from django.contrib import admin


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'question_type')


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


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):

    def questions_list(self, obj):

        questions = obj.questions.all()

        joined_questions = [
            f"{index}. {q.text}"
            for index, q in enumerate(questions, start=1)
        ]

        return "\n".join(joined_questions)

    questions_list.short_description = 'Вопросы теста'

    list_display = ('title', 'description', 'questions_list')

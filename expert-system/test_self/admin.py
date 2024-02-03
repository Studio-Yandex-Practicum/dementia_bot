from django.contrib import admin
from test_self.models import Answer, Session

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'test_id',
        'session_id', 'question_id',
        'text_answer', 'image_answer', 'ranking')


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'time_stamp'
    )

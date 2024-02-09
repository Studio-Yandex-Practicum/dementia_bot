from django.urls import path
from .views import answer_watch, answer_copy_test

urlpatterns = [
    path('api/answer_watch/', answer_watch, name='answer_watch'),
    path('api/answer_copy/', answer_copy_test, name='answer_copy'),
]

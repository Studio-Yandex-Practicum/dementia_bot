from django.urls import path

from .views import get_all_tests, get_test, submit_test,  get_result

urlpatterns = [
    path('api/tests/', get_all_tests, name='all_test'),
    path('api/test/<int:test_id>/', get_test, name='get_test'),
    path('api/submit/', submit_test, name='submit'),
    path('api/get_result/<int:telegram_id>/', get_result, name='get_result'),
]

from django.urls import path

from .views import (get_all_tests, get_test, submit_test,
                    submit_result, get_result, test_image)

urlpatterns = [
    path('api/tests/', get_all_tests, name='all_test'),
    path('api/test/<int:test_id>/', get_test, name='get_test'),
    path('api/submit/', submit_test, name='submit'),
    path('api/submit_result/', submit_result, name='submit_result'),
    path('api/get_result/<int:telegram_id>/', get_result, name='get_result'),
    # path для анализа ответа-изображения
    path('api/tests/<int:test_id>/sessions/<int:session_id>/answer/image/', test_image, name='test_image'),
]

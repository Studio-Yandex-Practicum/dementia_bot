from django.urls import path
from .views import get_test, submit_test

urlpatterns = [
    path('api/test/<int:test_id>/', get_test, name='get_test'),
    path('api/submit/', submit_test, name='submit')
]

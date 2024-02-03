from django.contrib import admin
from django.urls import include, path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from test_self.views import submit_text_answer, submit_image_answer, submit_session


schema_view = get_schema_view(
   openapi.Info(
      title="Бот - Деменция",
      default_version='v1',
      description="API бота, проверка ответов сервера",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,), # у кого должен быть доступ?
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
    path(
        'redoc/',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'
    ),
    path('api/tests/<int:test_id>/sessions/<int:session_id>/answer/text/', submit_text_answer, name='submit_text_answer'),
    path('api/tests/<int:test_id>/sessions/<int:session_id>/answer/image/', submit_image_answer, name='submit_image_answer'),
    path('api/tests/<int:test_id>/sessions/', submit_session, name = 'submit_session'),
    path('', include('botapp.urls')),
]

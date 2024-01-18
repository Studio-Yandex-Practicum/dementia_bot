from django.contrib import admin
from django.urls import include, path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


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
    path('', include('botapp.urls')),
]

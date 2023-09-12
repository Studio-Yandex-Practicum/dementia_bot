# expert-system

## Технологии
- [![Python](https://img.shields.io/badge/-Python3.10-464646?style=flat&logo=Python&logoColor=ffffff&color=043A6B)](https://www.python.org/)
- [![Django](https://img.shields.io/badge/-Python4.2.5-464646?style=flat&logo=Django&logoColor=ffffff&color=043A6B)](https://www.djangoproject.com)
- [![Postgresql](https://img.shields.io/badge/-Postgresql15-464646?style=flat&logo=Postgresql&logoColor=ffffff&color=043A6B)](https://www.postgresql.org)
- [![Nginx](https://img.shields.io/badge/-Nginx1.25-464646?style=flat&logo=Nginxl&logoColor=ffffff&color=043A6B)](https://www.nginx.com)

## Использование
Для разворачивания проекта должны быть установлены Docker, Docker Compose.
Проект будет развернут в 3-х контейнерах:
- прроект expert-system на Django
- база данных PostgresQL
- HTTP-сервер nginx

Клонируйте репозиторий и перейдите в проект expert-system

создайте .env файл
```
touch .env
```

шаблон наполнения env-файла 
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

DJANGO_SUPERUSER_PASSWORD=pass
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_USERNAME=admin
```

Запустите docker-compose
```
docker-compose up
```

Проект будет доступен по адресу http://127.0.0.1/
После установки для административной панели будет автоматически создан суперпользователь admin.
# dementia_bot
Бот для благотворительного фонда “ПАМЯТЬ ПОКОЛЕНИЙ”

## Технологии
- [![Aiogram](https://img.shields.io/badge/-Aiogram%203.0.0-464646?style=flat&logo=Nginxl&logoColor=ffffff&color=043A6B)](https://aiogram.dev)
- [![Django](https://img.shields.io/badge/-Python%204.2.5-464646?style=flat&logo=Django&logoColor=ffffff&color=043A6B)](https://www.djangoproject.com)
- [![Nginx](https://img.shields.io/badge/-Nginx%201.25-464646?style=flat&logo=Nginxl&logoColor=ffffff&color=043A6B)](https://www.nginx.com)
- [![Postgresql](https://img.shields.io/badge/-Postgresql%2015-464646?style=flat&logo=Postgresql&logoColor=ffffff&color=043A6B)](https://www.postgresql.org)
- [![Python](https://img.shields.io/badge/-Python%203.10-464646?style=flat&logo=Python&logoColor=ffffff&color=043A6B)](https://www.python.org/)

### 1. Подготовка

### Установка poetry
Важно:
- poetry ставится и запускается для каждого сервиса `bot`, `expert-system`
- для первого запуска проекта в контейнерах будет достаточно создать и активировать окружение в папке `expert-system`

1. Перейти в одну из папок сервиса, например:
```bash
cd expert-system
```
2. Затем выполните команды:

Для Linux, macOS, Windows (WSL):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```
Для Windows (Powershell):
```bash
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```
В macOS и Windows сценарий установки предложит добавить папку с исполняемым файлом Poetry в переменную PATH. Сделайте это, выполнив следующую команду (не забудьте поменять {USERNAME} на имя вашего пользователя):

macOS
```bash
export PATH="/Users/{USERNAME}/.local/bin:$PATH"
```
Windows
```bash
$Env:Path += ";C:\Users\{USERNAME}\AppData\Roaming\Python\Scripts"; setx PATH "$Env:Path"
```
Проверить установку:
```bash
poetry --version
```
Установка автодополнений bash (опционально):
```bash
poetry completions bash >> ~/.bash_completion
```
### Запуск проекта

1. Заполнить файлы .env согласно образцу:
шаблон наполнения env-файла 
```
telegram_api_token='1111111111:AAbbCcddEEFFgG1234567890'
WEBHOOK_MODE=False

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

2. В случае запуска проекта на Windows:
Рекомендуется установить "End of Line Sequence" LF в настройках точек входа "docker-entrypoint.sh" для обоих сервисов: `bot`, `expert-system`

3. Выполнить команду:

```
docker-compose -f ./infra/docker-compose.yaml up -d
```
### 2. Как это работает

1. Администрирование проекта будет доступно по адресу http://127.0.0.1/admin

2. Доступные команды бота: 

Команда для начала работы, приветствия и вывода списка доступных тестов
```
/start
```
Команда только для вывода списка доступных тестов
```
/selecttest
```
Команды для отмены
```
/cancel
```
```
отмена
```
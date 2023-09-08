# dementia_bot
бот для благотворительного фонда “ПАМЯТЬ ПОКОЛЕНИЙ”

## Подготовка

### 1. Установка poetry
Важно:
- poetry ставится и запускается для каждого сервиса `bot`, `expert-system` и `registration-system` отдельно
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

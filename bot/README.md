## dementia_bot

Бот для благотворительного фонда "ПАМЯТЬ ПОКОЛЕНИЙ".

### Подготовка к запуску

Перед запуском бота необходимо подготовить файл `.env`. Вы можете использовать образец `.env.example`, в котором прописаны все необходимые поля.

### Сборка и запуск контейнера

```bash
poetry run task start
```

### Описание функций

#### `display_question`

Отображает вопрос с клавиатурой в зависимости от типа вопроса.

```python
async def display_question(chat_id, message_id, question_text, question_type, bot):
    # ...
```

#### `cancel_handler`

Позволяет пользователю отменить любое действие.

```python
@question_router.message(Command("cancel"))
@question_router.message(F.text.casefold() == "отмена")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    # ...
```

#### `start_test`

Начинает тест, показывая список доступных тестов.

```python
@question_router.message(Command('selecttest'))
async def start_test(message: Message, state: FSMContext):
    # ...
```

#### `choose_test`

Выбирает тест и начинает отвечать на вопросы.

```python
@question_router.callback_query(Question.test)
async def choose_test(query: CallbackQuery, state: FSMContext):
    # ...
```

#### `questions`

Обрабатывает ответы на вопросы в тесте.

```python
@question_router.message(Question.answer)
async def questions(message: Message, state: FSMContext, bot: Bot):
    # ...
```

#### `answer_handler`

Обрабатывает ответы с использованием кнопок с действиями.

```python
@question_router.callback_query(
    AnswerCallback.filter(F.action.in_(
        [Action.yes, Action.no, Action.sometimes, Action.further])))
async def answer_handler(query: CallbackQuery, callback_data: AnswerCallback,
                         state: FSMContext, bot: Bot):
    # ...
```

#### `sex_handler`

Обрабатывает выбор пола.

```python
@question_router.callback_query(
    SexCallback.filter(F.action.in_([Sex.male, Sex.female])))
async def sex_handler(query: CallbackQuery, callback_data: SexCallback,
                      state: FSMContext, bot: Bot):
    # ...
```

#### `send_results_and_clear`

Отправляет результаты и очищает состояние.

```python
async def send_results_and_clear(state, bot, chat_id, message_id):
    # ...
```
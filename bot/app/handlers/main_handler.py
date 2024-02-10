from aiogram import Bot, Dispatcher, Router, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram.types import BotCommand, MenuButtonCommands
from aiogram.utils.markdown import hbold

router = Router()
dp = Dispatcher(bot=Bot, storage=MemoryStorage())


@router.message(Command("start"))
async def command_start(message: types.Message, bot: Bot):

    menu_commands = [
        BotCommand("/start", "Начать"),
        BotCommand("/help", "Помощь"),
        BotCommand("/test", "Пройти тест"),
        BotCommand("/signup", "Записаться в центр"),
        BotCommand("/participate", "Участвовать в мероприятиях"),
    ]

    await bot.set_chat_menu_button(
        chat_id=message.chat.id,
        menu_button=MenuButtonCommands(commands=menu_commands)
    )

    inline_kb = types.InlineKeyboardMarkup()

    inline_kb.row(
        types.InlineKeyboardButton(
            text="Пройти тест",
            callback_data="tests"
        ),
        types.InlineKeyboardButton(
            text="Записаться в центр",
            url="https://sber.xn--d1acamsh7dwd.net/"
        ),
        types.InlineKeyboardButton(
            text="Участвовать в мероприятиях",
            url="https://sber.деменция.net/"
        )
    )

    message_text = """
    Проект Деменция.net создан в  2021 году благотворительным фондом «Память поколений».

    Благотворительный фонд «Память поколений» был основан  22 июня  2015 года – в День памяти и скорби.

    Наш фонд помогает ветеранам Великой Отечественной войны и современных боевых действий (в Афганистане, Чечне, Сирии). Всего за время существования фонда мы помогли более  18000 ветеранам.

    Это огромное множество операций, курсов реабилитации, современных протезов и слуховых аппаратов, дорогостоящих колясок и комплектов медикаментов, средств личной гигиены. Но, что важнее, это тысячи изменившихся к лучшему жизней людей.

    Вы можете пройти тесты для проверки себя или близкого.
    """

    await message.answer(
        f"Здравствуйте, {hbold(message.from_user.full_name)}, {message_text}!",
        reply_markup=inline_kb
    )


@dp.callback_query_handler(lambda c: c.data == 'tests')
async def process_callback_test(callback_query: types.CallbackQuery, bot: Bot):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text="Вы можете выбрать один из тестов для прохождения: Проверь себя или Проверь близкого!",
        reply_markup=command_test()
    )


@router.message(Command("test"))
async def command_test(message: types.Message):

    inline_kb = types.InlineKeyboardMarkup()

    inline_kb.row(
        types.InlineKeyboardButton(
            text="Проверь себя",
            web_app=types.WebAppInfo(url="https://testing.xn--d1acamsh7dwd.net/testUser/1/")
        ),
        types.InlineKeyboardButton(
            text="Проверь близкого",
            web_app=types.WebAppInfo(url="https://testing2.xn--d1acamsh7dwd.net/testrelUser")
        )
    )

    await message.answer(
        "Вы можете выбрать один из тестов для прохождения: Проверь себя или Проверь близкого!",
        reply_markup=inline_kb
    )


@router.message(Command("help"))
async def command_help(message: types.Message):

    await message.answer("""
    С помощью команды /start вы можете запустить бота и пройти тесты!

    С помошью команды /test вы можете пройти тесты Проверь себя и Проверь близкого!

    С помощью команды /signup вы можете записаться в центр!

    С помощью команды /participate вы можете принять участие в мероприятиях!

    """)


@router.message(Command("/signup"))
async def command_signup(message: types.Message):

    inline_kb = types.InlineKeyboardMarkup()

    inline_kb.add(
        types.InlineKeyboardButton(
            text="Записаться в центр",
            url="https://sber.xn--d1acamsh7dwd.net/"
        )
    )

    await message.answer(
        "Нажмите на кнопку, чтобы записаться в центр!",
        reply_markup=inline_kb
    )


@router.message(Command("/participate"))
async def command_participate(message: types.Message):

    inline_kb = types.InlineKeyboardMarkup()

    inline_kb.add(
        types.InlineKeyboardButton(
            text="Участвовать в мероприятиях",
            url="https://sber.деменция.net/"
        )
    )

    await message.answer(
        "Нажмите на кнопку, чтобы участвовать в мероприятиях!",
        reply_markup=inline_kb
    )

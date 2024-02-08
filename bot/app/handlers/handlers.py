from aiogram import Bot, Router, types
from aiogram.filters import Command
from aiogram.types import BotCommand, MenuButtonCommands
from aiogram.utils.markdown import hbold

my_router = Router()


@my_router.message(Command("start"))
async def command_start(message: types.Message, bot: Bot):

    menu_commands = [
        BotCommand("/start", "Начать"),
        BotCommand("/help", "Помощь")
    ],

    await bot.set_chat_menu_button(
        chat_id=message.chat.id,
        menu_button=MenuButtonCommands(commands=menu_commands)
    )

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
    message_text = """\
    Проект Деменция.net создан в  2021 году благотворительным фондом «Память поколений».

    Благотворительный фонд «Память поколений» был основан  22 июня  2015 года – в День памяти и скорби.

    Наш фонд помогает ветеранам Великой Отечественной войны и современных боевых действий (в Афганистане, Чечне, Сирии). Всего за время существования фонда мы помогли более  18000 ветеранам.

    Это огромное множество операций, курсов реабилитации, современных протезов и слуховых аппаратов, дорогостоящих колясок и комплектов медикаментов, средств личной гигиены. Но, что важнее, это тысячи изменившихся к лучшему жизней людей.

    Вы можете пройти тесты для проверки себя или близкого.\
    """

    await message.answer(
        f"Здравствуйте, {hbold(message.from_user.full_name)}, {message_text}!",
        reply_markup=inline_kb
    )


@my_router.message(Command("help"))
async def command_help(message: types.Message):

    await message.answer("С помощью команды /start вы можете запустить бота и пройти тесты!")

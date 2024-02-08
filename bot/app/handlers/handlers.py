from aiogram import Bot, Router, types
from aiogram.filters import Command
from aiogram.utils.markdown import hbold

my_router = Router()


@my_router.message(Command("start"))
async def command_start(message: types.Message, bot: Bot):
    inline_kb = types.InlineKeyboardMarkup()
    inline_kb.row(
        types.InlineKeyboardButton("Проверь себя", url="https://testing.xn--d1acamsh7dwd.net/testUser/1/"),
        types.InlineKeyboardButton("Проверь близкого", url="https://testing2.xn--d1acamsh7dwd.net/testrelUser")
    )

    await bot.send_message(
        chat_id=message.chat.id,
        text=f"Здравствуйте, {hbold(message.from_user.full_name)}!",
        reply_markup=inline_kb
    )

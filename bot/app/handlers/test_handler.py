from datetime import datetime

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from validate_email import validate_email

from .test.keyboard import kb_gender
from .test.states import Register

form_router = Router()


@form_router.message(Command('test'))
async def register_(message: Message, state: FSMContext) -> None:
    await state.set_state(Register.name)
    await message.answer('Введите Ваше Имя:')


@form_router.message(Register.name)
async def get_name(message: Message, state: FSMContext) -> None:
    answer = message.text
    await state.update_data(name=answer)
    await state.set_state(Register.age)
    await message.answer('Введите свою Дату рождения:')


@form_router.message(Register.age)
async def get_age(message: Message, state: FSMContext):
    answer = message.text
    datetime.strptime(answer, '%d.%m.%Y')
    await state.update_data(age=answer)
    await state.set_state(Register.gender)
    await message.answer('Укажите Ваш Пол:', reply_markup=kb_gender)


@form_router.message(Register.gender)
async def get_gender(message: Message, state: FSMContext):
    answer = message.text
    if answer == 'Мужской' or answer == 'Женский':
        await state.update_data(gender=answer)
    else:
        await message.answer('Не соответствует вариантам: Мужской, Женский!!!')
        raise ValueError('Не соответствует вариантам!!!')
    await state.set_state(Register.email)
    await message.answer('Укажите электронную почту:')


@form_router.message(Register.email)
async def email(message: Message, state: FSMContext):
    answer = message.text
    if validate_email(answer) is True:
        await state.update_data(email=answer)
    else:
        await message.answer('Почта неверно написана. Попробуй снова.')
        raise ValueError('Неверное имя почты')
    data = await state.get_data()
    name = data.get('name')
    age = data.get('age')
    gender = data.get('gender')
    email = data.get('email')
    await message.answer('Твои ответы: '
                         f'Имя: {name}, '
                         f'дата рождения: {age}, '
                         f'пол - {gender}, почта - {email}')
    await state.finish()

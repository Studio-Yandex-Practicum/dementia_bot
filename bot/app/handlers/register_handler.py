from datetime import datetime

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from validate_email import validate_email

from .handler_constants import GENDER_CHOICES
from .states.states import Test
from app.handlers.keyboards.keyboard import kb_gender, markup_keyboard
from .validators.validator import validate_birthday

register_router = Router()


@register_router.message(Test.register_participant.name)
async def get_name(message: Message, state: FSMContext) -> None:
    answer = message.text
    # Добавить валидацию на ввод имени
    await state.update_data(name=answer)
    await state.set_state(Test.register_participant.age)
    await message.answer(
        'Введите Дату рождения респондента в формате ДД.ММ.ГГГГ:'
    )


@register_router.message(Test.register_participant.age)
async def get_age(message: Message, state: FSMContext):
    answer = message.text
    if not validate_birthday(answer):
        await message.answer(
            "Пожалуйста введите дату рождения в формате ДД.ММ.ГГГГ."
        )
        return
    answer = str(datetime.strptime(answer, '%d.%m.%Y').date())
    await state.update_data(birthdate=answer)
    await state.set_state(Test.register_participant.gender)
    await message.answer('Укажите Пол респондента:', reply_markup=kb_gender)


@register_router.message(Test.register_participant.gender)
async def get_gender(message: Message, state: FSMContext):
    answer = message.text
    if answer == 'Мужской' or answer == 'Женский':
        await state.update_data(gender=GENDER_CHOICES.get(answer))
    else:
        await message.answer('Не соответствует вариантам: Мужской, Женский!!!')
        return
    await state.set_state(Test.register_participant.email)
    await message.answer('Укажите свою электронную почту:',
                         reply_markup=ReplyKeyboardRemove(),)


@register_router.message(Test.register_participant.email)
async def email(message: Message, state: FSMContext):
    answer = message.text
    if validate_email(answer):
        await state.update_data(email=answer)
    else:
        await message.answer('Почта неверно написана. Попробуй снова.')
        return
    await state.set_state(Test.register_participant.occupation)
    await message.answer('Укажите образование/профессию респондента:')


@register_router.message(Test.register_participant.occupation)
async def email(message: Message, state: FSMContext):
    answer = message.text
    # Добавить валидацию ответа
    await state.update_data(occupation=answer)
    await state.set_state(Test.answers)
    data = await state.get_data()
    position = data.get('position')
    questions = data.get('questions')
    question_type = questions[position]['type']
    await message.answer(
            questions[position]['question'],
            reply_markup=markup_keyboard(
                question_type
            )
        )

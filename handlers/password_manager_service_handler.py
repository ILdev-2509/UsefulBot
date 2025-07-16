from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.keyboards import choosing_password_manager, back_button
from handlers.states import PasswordCheckerStates, PasswordGeneratorStates, MainStates
from config.client import client

router = Router()

@router.message(F.text == "Менеджер паролей")
async def converter_handler(message: Message, state: FSMContext) -> None:
    await message.answer(
        "🔐 <b>Менеджер паролей</b>\nВыберите действие:",
        reply_markup=choosing_password_manager,
    )
    await state.set_state(MainStates.choosing_password_manager)

@router.message(F.text == "Сгенерировать пароль", MainStates.choosing_password_manager)
async def bases_type_handler(message: Message, state: FSMContext) -> None:
    await message.answer(
        "🔢 <b>Генератор паролей</b>\nВведите длину пароля (от 8 до 64 символов):",
        reply_markup=back_button(),
    )
    await state.set_state(PasswordCheckerStates.waiting_for_input)
    
@router.message(PasswordCheckerStates.waiting_for_input)
async def bases_output_handler(message: Message) -> None:
    result = client.generate_password(length=message.text)
    await message.answer(
        f"🔑 <b>Ваш пароль:</b>\n<code>{result}</code>",
    )

@router.message(F.text == "Проверка надежности пароля")
async def bases_type_handler(message: Message, state: FSMContext) -> None:
    await message.answer(
        "🛡️ <b>Проверка пароля</b>\nВведите пароль для анализа:",
        reply_markup=back_button(),
    )
    await state.set_state(PasswordGeneratorStates.waiting_for_input)


@router.message(PasswordGeneratorStates.waiting_for_input)
async def password_check_handler(message: Message) -> None:
    result = client.check_password(
        password=message.text
    )
    problems = result.get('problems', [])
    if problems:
        problems_formatted = "\n".join(f"• {problem}" for problem in problems)
        response = (
            f"🔐 <b>Проверка пароля</b>\n\n"
            f"<b>Общая оценка:</b> {result['score']}/10\n"
            f"<b>Обнаруженные проблемы:</b>\n{problems_formatted}"
        )
    else:
        response = (
            f"🔐 <b>Проверка пароля</b>\n\n"
            f"<b>Общая оценка:</b> {result['score']}/10\n"
            f"✅ <b>Пароль идеален! Не обнаружено проблем</b>"
        )
    await message.answer(response)
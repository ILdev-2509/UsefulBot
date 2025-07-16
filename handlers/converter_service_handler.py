from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.keyboards import choosing_converter, choosing_direction, back_button
from handlers.states import BaseConverterStates, RomanConverterStates, MainStates
from config.client import client

router = Router()

roman_directions = ["Арабские → Римские", "Римские → Арабские"]

@router.message(F.text == "Конвертер")
async def converter_handler(message: Message, state: FSMContext) -> None:
    await message.answer(
        "🔄 <b>Конвертеры</b>\nВыберите нужный вам конвертер:",
        reply_markup=choosing_converter,
    )
    await state.set_state(MainStates.choosing_converter)

@router.message(F.text == "Римские цифры")
async def roman_type_handler(message: Message, state: FSMContext) -> None:
    await message.answer(
        "🏛️ <b>Римские цифры</b>\nВыберите направление конвертации:",
        reply_markup=choosing_direction(roman_directions),
    )
    await state.set_state(RomanConverterStates.waiting_for_direction)

@router.message(F.text.in_(roman_directions), RomanConverterStates.waiting_for_direction)
async def roman_input_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(direction=message.text)
    await message.answer(
        "🔢 Введите число для конвертации:",
        reply_markup=back_button()
    )
    await state.set_state(RomanConverterStates.waiting_for_input)

@router.message(RomanConverterStates.waiting_for_input)
async def roman_output_handler(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    direction = data['direction']

    if direction == roman_directions[0]:
        result = client.convert_to_roman(number=message.text)
    else:
        result = client.convert_from_roman(number=message.text)

    await message.answer(
        f"🔄 <b>Результат:</b>\n<code>{result}</code>",
    )

@router.message(F.text == "Системы счисления")
async def bases_type_handler(message: Message, state: FSMContext) -> None:
    await message.answer(
        "🔢 <b>Конвертер систем счисления</b>\n"
        "Введите через пробел:\n"
        "1. Исходное основание (2-36)\n"
        "2. Требуемое основание (2-36)\n"
        "3. Число для конвертации\n\n"
        "<i>Пример: 10 16 255</i>",
        reply_markup=back_button(),
    )
    await state.set_state(BaseConverterStates.waiting_for_input)
    
@router.message(BaseConverterStates.waiting_for_input)
async def bases_output_handler(message: Message) -> None:
    data = message.text.split(" ")
    result = client.convert_bases(from_base=data[0], to_base=data[1], number=data[2])
    await message.answer(
        f"🔄 <b>Результат конвертации:</b>\n"
        f"<code>{result}</code>",
    )

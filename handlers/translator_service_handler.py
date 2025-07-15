from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.keyboards import choosing_translator, choosing_direction, back_button
from handlers.states import MorseTranslatorStates, KeyboardTranslatorStates, MainStates
from config.client import client

router = Router()

keyboard_directions = ["С русской на английскую", "С английской на русскую"]
morse_directions = ["С русского на морзе", "С морзе на русский"]

@router.message(F.text == "Переводчик")
async def converter_handler(message: Message, state: FSMContext) -> None:
    await message.answer(
        "🌐 <b>Выберите переводчик:</b>",
        reply_markup=choosing_translator,
    )
    await state.set_state(MainStates.choosing_translator)

@router.message(F.text == "Переводчик клавиатуры")
async def keyboard_translator_handler(message: Message, state: FSMContext) -> None:
    await message.answer(
        "⌨️ <b>Переводчик клавиатуры</b>\nВыберите направление перевода:",
        reply_markup=choosing_direction(keyboard_directions),
    )
    await state.set_state(KeyboardTranslatorStates.waiting_for_direction)

@router.message(F.text.in_(keyboard_directions), KeyboardTranslatorStates.waiting_for_direction)
async def keyboard_input_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(direction='to_russian' if message.text == keyboard_directions[1] else 'to_english')
    await message.answer(
        "⌨️ Введите текст для перевода:",
        reply_markup=back_button()
    )
    await state.set_state(KeyboardTranslatorStates.waiting_for_input)

@router.message(KeyboardTranslatorStates.waiting_for_input)
async def keyboard_output_handler(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    direction = data['direction']
    result = client.translate_keyboard(direction=direction, text=message.text)
    await message.answer(
        f"🔤 <b>Результат:</b>\n<code>{result}</code>",
    )

@router.message(F.text == "Переводчик морзе")
async def morse_translator_handler(message: Message, state: FSMContext) -> None:
    await message.answer(
        "📻 <b>Азбука Морзе</b>\nВыберите направление перевода:",
        reply_markup=choosing_direction(morse_directions),
    )
    await state.set_state(MorseTranslatorStates.waiting_for_direction)

@router.message(F.text.in_(morse_directions), MorseTranslatorStates.waiting_for_direction)
async def morse_input_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(direction=message.text)
    await message.answer(
        "📻 Введите текст для перевода:",
        reply_markup=back_button()
    )
    await state.set_state(MorseTranslatorStates.waiting_for_input)

@router.message(MorseTranslatorStates.waiting_for_input)
async def morse_output_handler(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    direction = data['direction']
    if direction == morse_directions[0]:
        result = client.translate_to_morse(text=message.text)
    else:
        result = client.translate_from_morse(text=message.text)

    await message.answer(
        f"📡 <b>Результат:</b>\n<code>{result}</code>",
    )

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from keyboards.keyboards import main_menu

router = Router()

@router.message(Command("start"))
async def start_handler(message: Message) -> None:
    await message.answer(
        text=(
            f"👋 <b>Добро пожаловать, "
            f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>!</b>\n\n"
            "🚀 Я ваш многофункциональный помощник с различными инструментами:\n\n"
            "• 🔤 Переводчики текста\n"
            "• 🔢 Конвертеры систем счисления\n"
            "• 🔐 Генератор и проверка паролей\n\n"
            "👉 Для начала работы просто выберите нужный инструмент в меню!\n"
            "ℹ️ Справка: /help"
        ),
        reply_markup=main_menu,
    )

@router.message(Command("help"))
async def help_handler(message: Message) -> None:
    await message.answer(
        text=(
            "🛠 <b>Справочник по функциям бота</b>\n\n"

            "🔤 <b>Переводчики:</b>\n"
            "   • <b>Морзе ↔ Текст</b>\n"
            "      → 📡 Кодирование текста в азбуку Морзе\n"
            "      → 🔊 Декодирование азбуки Морзе в текст\n\n"

            "   • <b>Раскладка клавиатуры</b>\n"
            "      → 🇬🇧 Английская → Русская\n"
            "      → 🇷🇺 Русская → Английская\n\n"

            "🔢 <b>Конвертеры:</b>\n"
            "   • <b>Системы счисления</b>\n"
            "      → 🔄 Конвертация между основаниями (2-36)\n"
            "      → <i>Пример: 10 16 255 → FF</i>\n\n"

            "   • <b>Римские цифры</b>\n"
            "      → 1️⃣2️⃣ Арабские → Римские\n"
            "      → 🏛️ Римские → Арабские\n\n"

            "🔑 <b>Менеджер паролей:</b>\n"
            "   • <b>Генератор</b>\n"
            "      → 🔐 Создание надежных паролей\n"
            "      → ⚙️ Настройка длины (8-64 символа)\n\n"

            "   • <b>Проверка сложности</b>\n"
            "      → 🛡️ Анализ надежности пароля\n"
            "      → 💯 Оценка от 0 до 10\n"
            "      → ❗ Вывод обнаруженных проблем\n\n"

            "⚙️ <b>Техническая информация:</b>\n"
            "   • Все запросы обрабатываются через API\n"
            "   • ⏱️ Максимальное время ответа: 30 секунд\n"
            "   • 🎛️ Для работы используйте клавиатуру\n\n"

            "🆘 <b>Если возникли проблемы:</b>\n"
            "   • 🔄 Повторите действие, проверив ввод\n"
            "   • ⏳ При отсутствии ответа - попробуйте позже\n"
            "   • 📣 О критических ошибках сообщайте в поддержку"
        ),
    )

@router.message(Command("cancel"))
@router.message(F.text.lower() == "отмена")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    if current_state is None:
        await message.answer(
            "🤷‍♂️ <b>Сейчас нечего отменять</b>\n"
            "Выберите действие в главном меню:",
            reply_markup=main_menu,
        )
        return
    await state.clear()

    await message.answer(
        "❌ <b>Операция отменена</b>",
        reply_markup=ReplyKeyboardRemove(),
    )

    await message.answer(
        "⬇️ <b>Вы вернулись в главное меню:</b>",
        reply_markup=main_menu,
    )

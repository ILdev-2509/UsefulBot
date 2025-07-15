from aiogram.types import ErrorEvent, Message, CallbackQuery
from aiogram import Router
from requests import HTTPError
from config.loader import settings
from config.bot import bot

router = Router()


@router.error()
async def global_error_handler(event: ErrorEvent) -> bool | None:
    update = event.update
    exception = event.exception

    if not isinstance(exception, HTTPError):
        user_info = "Неизвестный пользователь"
        message_text = "Нет текста"
        user_id = None

        if update.message:
            source: Message = update.message
            user_id = source.from_user.id
            user_info = f"<a href='tg://user?id={user_id}'>{source.from_user.full_name}</a>"
            message_text = source.text or "Нет текста"
        elif update.callback_query:
            source: CallbackQuery = update.callback_query
            user_id = source.from_user.id
            user_info = f"<a href='tg://user?id={user_id}'>{source.from_user.full_name}</a>"
            message_text = source.data or "Нет данных"

        tb = f"{type(exception).__name__}: {str(exception)}"

        await bot.send_message(
            chat_id=settings.CHAT_ID,
            text=(
                "🚨 <b>Ошибка в боте</b>\n"
                f"<b>Пользователь:</b> {user_info}\n"
                f"<b>ID:</b> <code>{user_id}</code>\n"
                f"<b>Сообщение:</b> <code>{message_text}</code>\n"
                f"<b>Ошибка:</b> <pre>{tb}</pre>"
            ),
            parse_mode="HTML"
        )

        if user_id:
            try:
                await bot.send_message(
                    chat_id=user_id,
                    text="⚠️ Произошла непредвиденная ошибка при обработке вашего запроса. "
                         "Разработчики уже уведомлены. Пожалуйста, попробуйте позже."
                )
            except Exception:
                pass
        return True
    return None
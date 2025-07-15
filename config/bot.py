from aiogram import Bot
from aiogram.client.default import DefaultBotProperties

from config.loader import settings

bot = Bot(
    token=settings.TELEGRAM_BOT_TOKEN.get_secret_value(),
    default=DefaultBotProperties(parse_mode="HTML")
)


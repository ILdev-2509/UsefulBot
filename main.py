import asyncio
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.strategy import FSMStrategy

from config.bot import bot
from handlers.error_handler import router as error_router
from handlers.main_commands_handler import router as main_router
from handlers.converter_service_handler import router as converters_router
from handlers.translator_service_handler import router as translator_router
from handlers.password_manager_service_handler import router as password_manager_router

async def main() -> None:
    dp = Dispatcher(
        storage=MemoryStorage(), 
        fsm_strategy=FSMStrategy.USER_IN_CHAT
    )
    dp.include_routers(
        error_router,
        main_router,
        converters_router,
        translator_router,
        password_manager_router
    )
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import threading
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.strategy import FSMStrategy
from http.server import BaseHTTPRequestHandler, HTTPServer

from config.bot import bot
from handlers.error_handler import router as error_router
from handlers.main_commands_handler import router as main_router
from handlers.converter_service_handler import router as converters_router
from handlers.translator_service_handler import router as translator_router
from handlers.password_manager_service_handler import router as password_manager_router

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')

def run_health_check_server():
    server = HTTPServer(('0.0.0.0', 8443), HealthCheckHandler)
    server.serve_forever()

async def main() -> None:
    threading.Thread(target=run_health_check_server, daemon=True).start()

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

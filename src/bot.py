import asyncio
import logging
import os
import sys
from .handlers import client
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

load_dotenv()

dp = Dispatcher()

async def main() -> None:
    dp.include_router(client.router)
    bot = Bot(os.getenv("TOKEN"))

    await dp.start_polling(bot)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
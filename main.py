import asyncio
import logging
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
# from apscheduler.schedulers.asyncio import AsyncIOScheduler

from core.handlers import services, steps
from core.keyboards.menu_commands import menu_commands

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')


async def run_bot():
    logging.basicConfig(
        level=logging.INFO
    )

    bot = Bot(BOT_TOKEN, parse_mode='HTML')
    dp = Dispatcher()

    dp.include_router(services.router)
    dp.include_router(steps.router)

    await menu_commands(bot)

    try:
        await bot.delete_webhook(drop_pending_updates=True)  #
        await dp.start_polling(bot)

    finally:
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(run_bot())

    except (KeyboardInterrupt, SystemExit):
        print('Error')

import os

from aiogram import Bot, Router
from dotenv import load_dotenv

load_dotenv()
ADMIN_ID = os.getenv('ADMIN_ID')

router = Router()


@router.startup()
async def startup(bot: Bot):
    await bot.send_message(chat_id=ADMIN_ID, text='Started')


@router.shutdown()
async def shutdown(bot: Bot):
    await bot.send_message(chat_id=ADMIN_ID, text='Stopped')

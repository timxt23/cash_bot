from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def menu_commands(bot: Bot):
    commands = [
        BotCommand(
            command="start",
            description='Запустить бота'
        ),
        BotCommand(
            command='new_operation',
            description='Новая запись 📝'
        ),
        BotCommand(
            command='help',
            description='О боте ❓'
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
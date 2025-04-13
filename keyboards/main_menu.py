from aiogram import Bot
from aiogram.types import BotCommand


async def main_menu(bot: Bot):
    commands = await bot.set_my_commands([
        BotCommand(
            command="/start",
            description="Start bot."
        ),
        BotCommand(
            command="/cancel",
            description="Reset bot state."
        )
    ])

    return commands

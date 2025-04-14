from pathlib import Path
from aiogram import Bot
from typing import BinaryIO


async def load_object_from_telegram_api(bot: Bot, file_id: str) -> BinaryIO:
    file = await bot.get_file(file_id=file_id)
    uploaded_file = await bot.download_file(file_path=file.file_path)
    uploaded_file.name = Path(file.file_path)
    return uploaded_file

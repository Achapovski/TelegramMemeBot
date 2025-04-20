import io
from mimetypes import guess_type
from pathlib import Path
from aiogram import Bot
from typing import BinaryIO
from zipfile import ZipFile, ZIP_DEFLATED


async def load_object_from_telegram_api(bot: Bot, file_id: str) -> BinaryIO:
    file = await bot.get_file(file_id=file_id)
    file_path = Path(file.file_path)
    uploaded_file = await bot.download_file(file_path=file.file_path)

    if not is_valid_mime_type(file_path.name):
        uploaded_file = convert_to_zip(uploaded_file, file_path.name)
        file_path = Path(file_path.stem + ".zip")

    uploaded_file.name = file_path
    return uploaded_file


def is_valid_mime_type(file_name_with_ext: str):
    type_, subtype = guess_type(file_name_with_ext)[0].split("/")
    if (
            type_ == "application" and subtype not in ("zip", "pdf")) or (
            type_ == "video" and subtype not in ("html", "mp4")
    ):
        return False
    return True


def convert_to_zip(file: BinaryIO, file_name_with_ext: str):
    buffer_file = io.BytesIO()

    file_name_with_ext = Path(file_name_with_ext)
    name, extension = file_name_with_ext.stem, file_name_with_ext.suffix

    with ZipFile(file=buffer_file, mode="w", compression=ZIP_DEFLATED) as zipfile:
        zipfile.writestr(zinfo_or_arcname=f"{name}{extension}", data=file.read())

    buffer_file.seek(0)
    return buffer_file

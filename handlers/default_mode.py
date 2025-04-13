from typing import Union

from aiogram import Router, Bot

from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message

from clients.S3 import S3Client
from handlers.states import FSMStatest, FSMTestState
from repositories import UserRepository
from repositories.files import FileRepository
from services.auto_delete_msg_service import DeleteMessageService
from utils.inspections import get_file_from_message

router = Router()


@router.message(Command("cancel"), ~StateFilter(default_state))
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Canceled")


@router.message(CommandStart(), StateFilter(default_state))
async def print_welcome(message: Message, usr_repo: UserRepository, state: FSMContext):
    await usr_repo.add_user(user_id=message.from_user.id)
    # await state.set_state(FSMTestState.moke)
    await state.set_state(FSMStatest.add_meme)
    await message.answer("Send me voice meme.")


@router.message(StateFilter(FSMStatest.add_meme))
async def print_update_type(message: Message, state: FSMContext):
    data = {**get_file_from_message(message), "prefix": message.from_user.id}

    await message.answer("Ok, let`s continue")
    await state.update_data(data=data)
    await state.set_state(FSMStatest.add_meme_title)


@router.message(StateFilter(FSMStatest.add_meme_title))
async def get_meme_title(message: Message, obj_repo: S3Client, state: FSMContext, file_repo: FileRepository, bot: Bot):
    data = await state.get_data()

    # FIXME: Вынести в отдельную утилиту
    if data.get("file_extension"):
        file = await bot.get_file(file_id=data["file"])
        uploaded_file = await bot.download_file(file_path=file.file_path)

        data.update({
            "file": uploaded_file,
            "file_extension": file.file_path.split(".")[-1] if data.get("type") != "photo" else "jpeg",
        })

    prefix, key = await obj_repo.upload_object(**data, file_name=message.text)
    obj_url = await obj_repo.get_object_from_public_container(key=key, prefix=prefix)

    await file_repo.add_file(title=message.text, url=obj_url, owner_id=message.from_user.id, type_=data.get("type"))

    await message.answer("Created!")
    await state.clear()
    await state.set_state(FSMStatest.add_meme)


@router.message(StateFilter(FSMTestState.moke))
async def test_handler(message: Message, msg_service: DeleteMessageService):
    await message.answer("Ok")

from aiogram import Router, Bot

from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message

from custom_types import ObjectType
from handlers.states import FSMStatest, FSMTestState
from repositories import UserRepository
from repositories.files import FileRepository
from schemes.types.types import FileMeta
from services import ObjectLoadService
from utils.inspections import get_file_from_message
from utils.loaders import load_object_from_telegram_api

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
    file_meta = get_file_from_message(message)

    if file_meta.type is ObjectType.undefined.value:
        return await message.answer("Please, send me a photo or voice message")

    await message.answer("Ok, let`s continue")
    await state.update_data(data={"file_meta": file_meta.model_dump()})
    await state.set_state(FSMStatest.add_meme_title)


@router.message(StateFilter(FSMStatest.add_meme_title))
async def get_meme_title(message: Message, obj_service: ObjectLoadService,
                         state: FSMContext, file_repo: FileRepository, bot: Bot):
    file_meta = await state.get_data()
    file_meta = FileMeta(**file_meta.get("file_meta"))
    file = await load_object_from_telegram_api(bot=bot, file_id=file_meta.id)

    key = await obj_service.upload_object(
        key=message.text.title() + file.name.suffix,
        obj=file,
        unique_prefix=str(message.from_user.id)
    )

    obj_url = await obj_service.download_object(key=key.key, unique_prefix=key.prefix)
    await file_repo.add_file(title=message.text.title(), url=obj_url,
                             owner_id=message.from_user.id, type_=file_meta.type)

    await message.answer("Created!")
    await state.clear()
    await state.set_state(FSMStatest.add_meme)


@router.message(StateFilter(FSMTestState.moke))
async def test_handler(message: Message):
    await message.answer("Ok")

import logging

from aiogram import Router, Bot

from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message
from fluentogram import TranslatorRunner

from custom_types import ObjectType
from handlers.states import FSMStatest, FSMTestState
from repositories import UserRepository
from repositories.files import FileRepository
from schemes.types.types import FileMeta
from services import ObjectLoadService
from utils.inspections import get_file_from_message
from utils.loaders import load_object_from_telegram_api

router = Router()


@router.message(Command("cancel"))
async def cancel_process_handler(message: Message, state: FSMContext, i18n: TranslatorRunner):
    await message.answer(i18n.message())
    await state.clear()
    await message.answer("Canceled")


@router.message(CommandStart(), StateFilter(default_state))
async def welcome_process_handler(message: Message, usr_repo: UserRepository, state: FSMContext):
    await usr_repo.add_user(user_id=message.from_user.id)
    # await state.set_state(FSMTestState.moke)
    await state.set_state(FSMStatest.add_meme)
    await message.answer("Send me voice meme.")


@router.message(StateFilter(FSMStatest.add_meme))
async def send_meme_process_handler(message: Message, state: FSMContext):
    file_meta: FileMeta = get_file_from_message(message)

    if file_meta.type is ObjectType.undefined.value:
        return await message.answer("Please, send me a photo or voice message")

    await message.answer("Ok, let`s continue")
    await state.update_data(data={"file_meta": file_meta.model_dump()})
    await state.set_state(FSMStatest.add_meme_title)


@router.message(StateFilter(FSMStatest.add_meme_title))
async def send_meme_title_process_handler(message: Message, obj_service: ObjectLoadService,
                                          state: FSMContext, file_repo: FileRepository, bot: Bot):
    file_meta = FileMeta(**await state.get_value("file_meta"))
    file = await load_object_from_telegram_api(bot=bot, file_id=file_meta.id)

    try:
        key = await obj_service.upload_object(
            key=message.text.title() + file.name.suffix,
            obj=file,
            unique_prefix=str(message.from_user.id)
        )

        # FIXME: Реализовать транзакцию с добавлением файла в БД и SSS
        obj_url = await obj_service.get_object_url(key=key.key, unique_prefix=key.prefix)
        await file_repo.add_file(title=message.text.title(), url=obj_url,
                                 owner_id=message.from_user.id, type_=file_meta.type)
    except (Exception, ) as err:
        logging.error("Error on create/update object %s" % err)

    await message.answer("Created!")
    await state.clear()
    await state.set_state(FSMStatest.add_meme)


@router.message()
async def track_other_message_process_handler(message: Message):
    await message.answer("You should be on work state of bot ('Send me /start')")


@router.message(StateFilter(FSMTestState.moke))
async def test_handler(message: Message):
    await message.answer("Ok")

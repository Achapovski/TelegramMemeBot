import logging

from aiogram import Bot
from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput

from custom_types import ObjectType
from repositories.files import FileRepository
from schemes.types.types import FileMeta
from services import ObjectLoadService
from utils.inspections import get_file_from_message
from utils.loaders import load_object_from_telegram_api
from utils.wrappers import DialogDataKwargsDecorator


async def validate_message_type(message: Message, message_input: MessageInput, dialog_manager: DialogManager, **kwargs):
    file_meta: FileMeta = get_file_from_message(message)

    if is_known_type := not (file_meta.type is ObjectType.undefined.value):
        await dialog_manager.next()

    dialog_manager.dialog_data.update({"file_meta": file_meta.model_dump(), "is_valid_meme_type": is_known_type})


@DialogDataKwargsDecorator("bot", "obj_service", "file_repo")
async def validate_meme_title(message: Message, message_input: MessageInput, dialog_manager: DialogManager,
                              bot: Bot, obj_service: ObjectLoadService, file_repo: FileRepository,  **kwargs):
    file_meta = FileMeta(**dialog_manager.dialog_data.get("file_meta"))
    file = await load_object_from_telegram_api(bot=bot, file_id=file_meta.id)

    if not message.text:
        dialog_manager.dialog_data["obj_is_created"] = "invalid"
        return

    valid_key = ((clean_title := message.text.title()) + file.name.suffix)

    # FIXME: Реализовать транзакцию с добавлением файла в БД и SSS
    try:
        key = await obj_service.upload_object(key=valid_key, obj=file, unique_prefix=str(message.from_user.id))
        obj_url = await obj_service.get_object_url(key=key.key, unique_prefix=key.prefix)
        await file_repo.add_file(title=clean_title, url=obj_url, owner_id=message.from_user.id, type_=file_meta.type)
    except (Exception,) as err:
        logging.error("Error on create/update object %s" % err)
        dialog_manager.dialog_data["obj_is_created"] = False
    else:
        dialog_manager.dialog_data["obj_is_created"] = True

    # await dialog_manager.switch_to(WorkingDialogStates.add_meme_object)
    # dialog_manager.dialog_data.clear()

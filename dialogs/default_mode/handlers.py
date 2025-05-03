import json

from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner

from custom_types.enums import LocalesEnum
from dialogs.dialog_states import WorkingDialogStates, SettingsStates
from dialogs.dialog_types import UserSettingsScheme
from repositories import UserRepository
from services import CacheService

router = Router()
# TODO: доработать отмену состояния диалога в каждом обработчике


@router.message(CommandStart())
async def welcome_getter(message: Message, usr_repo: UserRepository, dialog_manager: DialogManager):
    if dialog_manager.current_stack().intents:
        await dialog_manager.done()
    language = message.from_user.language_code

    if not usr_repo.info.get_user_info(user_id=message.from_user.id):
        await usr_repo.add_user(user_id=message.from_user.id, language=getattr(LocalesEnum, language))

    await dialog_manager.start(WorkingDialogStates.add_meme_object)


@router.message(Command("cancel"))
async def cancel_process_handler(message: Message, dialog_manager: DialogManager, i18n: TranslatorRunner):
    if dialog_manager.current_stack().intents:
        await dialog_manager.done()
    await dialog_manager.start(WorkingDialogStates.add_meme_object)


@router.message(Command("settings"))
async def settings_process_handler(message: Message, dialog_manager: DialogManager,
                                   usr_repo: UserRepository, cache_service: CacheService):
    cache_data = await cache_service.from_cache(key=message.from_user.id, shadow=True)
    if cache_data:
        print("FROM CACHE")
        user_settings = UserSettingsScheme.model_validate(json.loads(cache_data)).model_dump()
    else:
        print("FROM DB")
        user = await usr_repo.settings.get_user_settings(user_id=message.from_user.id)
        user_settings = UserSettingsScheme.model_validate(user.model_dump(exclude={"id"})).model_dump()

    if dialog_manager.current_stack().intents:
        await dialog_manager.done()

    await dialog_manager.start(SettingsStates.edit_settings, data={"user_settings": user_settings})

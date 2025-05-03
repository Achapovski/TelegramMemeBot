from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from dialogs.dialog_types import UserSettingsScheme
from services import CacheService
from dialogs.dialog_states import SettingsStates
from utils.wrappers import DialogDataKwargsDecorator


async def on_lang_btn_click(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(SettingsStates.choice_language)


async def on_dialog_btn_click(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(SettingsStates.choice_dialog_type)


@DialogDataKwargsDecorator("radio_lang", "radio_dialog", "cache_service", global_=True)
async def on_confirm_back_btn_click(callback: CallbackQuery, button: Button, dialog_manager: DialogManager,
                                    cache_service: CacheService, radio_lang: str, radio_dialog: str):

    old_user_settings = UserSettingsScheme.model_validate(dialog_manager.start_data.get("user_settings"))
    actual_user_lang = radio_lang or old_user_settings.language_locale
    actual_user_dialog = radio_dialog or old_user_settings.dialog_type
    new_user_setting = UserSettingsScheme(language_locale=actual_user_lang, dialog_type=actual_user_dialog)

    await cache_service.to_cache(
        key=callback.from_user.id, value=new_user_setting.model_dump_json(), exp_time=10, shadow=True
    )


async def confirm_btn_click(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    user_settings = UserSettingsScheme.model_validate(dialog_manager.start_data.get("user_settings"))
    await dialog_manager.switch_to(SettingsStates.edit_settings)

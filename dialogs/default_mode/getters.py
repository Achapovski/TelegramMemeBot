from aiogram import Router

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import ManagedRadio
from fluentogram import TranslatorRunner, TranslatorHub

from custom_types.enums import LocalesEnum, DialogsTypeEnum
from dialogs.dialog_types import UserSettingsScheme
from utils.wrappers import DialogDataKwargsDecorator

router = Router()


async def welcome_getter(i18n: TranslatorRunner, dialog_manager: DialogManager):
    match dialog_manager.dialog_data.get("is_valid_meme_type"):
        case None:
            return {"message": i18n.message.welcome()}
        case False:
            return {"message": i18n.object.invalid()}
        case True:
            return {"message": i18n.object.valid()}


async def meme_title_getter(i18n: TranslatorRunner, dialog_manager: DialogManager):
    match dialog_manager.dialog_data.get("obj_is_created"):
        case None:
            return {"message": i18n.object.valid()}
        case "invalid":
            return {"message": i18n.object.invalid_title()}
        case False:
            return {"message": i18n.object.not_created()}
        case True:
            return {"message": i18n.object.created()}


@DialogDataKwargsDecorator("_translator", "user_settings")
async def settings_getter(_translator: TranslatorHub, user_settings: dict):
    settings: UserSettingsScheme = UserSettingsScheme.model_validate(user_settings)
    i18n: TranslatorRunner = _translator.get_translator_by_locale(settings.language_locale)

    language_setting = i18n.settings.locale_type()
    dialog_setting = i18n.settings.dialog_type()
    message = i18n.settings.labels.settings()
    button = i18n.buttons.confirm()

    return {"message": message, "language": language_setting, "dialog": dialog_setting, "confirm_back": button}


@DialogDataKwargsDecorator("_translator", "radio_lang", "user_settings", global_=True, checking_=False)
async def languages_getter(dialog_manager: DialogManager, _translator: TranslatorHub,
                           user_settings: dict, radio_lang: ManagedRadio):
    settings = UserSettingsScheme.model_validate(user_settings)
    i18n: TranslatorRunner = _translator.get_translator_by_locale(settings.language_locale)

    if not radio_lang.get_checked():
        await radio_lang.set_checked(settings.language_locale)

    dialog_manager.dialog_data["radio_lang"] = radio_lang.get_checked()

    languages = [(lang.name, lang.name) for lang in LocalesEnum]
    message = i18n.settings.labels.locale_type()
    confirm_back = i18n.buttons.confirm()
    return {"message": message, "languages": languages, "confirm_back": confirm_back}


@DialogDataKwargsDecorator("radio_dialog", "_translator", "user_settings", global_=True, checking_=False)
async def dialogs_getter(dialog_manager: DialogManager, _translator: TranslatorHub,
                         user_settings: dict, radio_dialog: ManagedRadio):
    settings = UserSettingsScheme.model_validate(user_settings)
    i18n: TranslatorRunner = _translator.get_translator_by_locale(settings.language_locale)

    if not radio_dialog.get_checked():
        await radio_dialog.set_checked(settings.dialog_type)

    dialog_manager.dialog_data["radio_dialog"] = radio_dialog.get_checked()

    dialogs = [(dialog.value, dialog.name) for dialog in DialogsTypeEnum]
    message = i18n.settings.labels.dialog_type()
    confirm_back = i18n.buttons.confirm()
    return {"message": message, "dialogs": dialogs, "confirm_back": confirm_back}

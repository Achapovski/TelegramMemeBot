from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Button, Radio
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.input import MessageInput

from dialogs.default_mode.callbacks import on_lang_btn_click, on_dialog_btn_click, on_confirm_back_btn_click, \
    confirm_btn_click
from dialogs.dialog_pre_handlers import validate_message_type, validate_meme_title
from dialogs.dialog_states import WorkingDialogStates, SettingsStates
from dialogs.default_mode.getters import welcome_getter, meme_title_getter, settings_getter, languages_getter, \
    dialogs_getter

working_dialog = Dialog(
    Window(
        Format(text="{message}"),
        MessageInput(func=validate_message_type),
        getter=welcome_getter,
        state=WorkingDialogStates.add_meme_object,
    ),
    Window(
        Format(text="{message}"),
        MessageInput(func=validate_meme_title),
        getter=meme_title_getter,
        state=WorkingDialogStates.add_meme_title,
    )
)

settings_dialog = Dialog(
    Window(
        Format("{message}"),
        Button(
            text=Format("{language}"),
            id="language_button",
            on_click=on_lang_btn_click,
        ),
        Button(
            text=Format("{dialog}"),
            id="dialog_button",
            on_click=on_dialog_btn_click,
        ),
        Button(
            text=Format("{confirm_back}"),
            id="back_or_confirm_button",
            on_click=on_confirm_back_btn_click
        ),
        getter=settings_getter,
        state=SettingsStates.edit_settings
    ),
    Window(
        Format("{message}"),
        Radio(
            checked_text=Format("🔘{item[0]}"),
            unchecked_text=Format("⚪️{item[0]}"),
            id="radio_lang",
            item_id_getter=lambda x: x[1],
            items="languages",
        ),
        Button(
            text=Format("{confirm_back}"),
            id="confirm_button",
            on_click=confirm_btn_click
        ),
        getter=languages_getter,
        state=SettingsStates.choice_language
    ),
    Window(
        Format("{message}"),
        Radio(
            checked_text=Format("🔘{item[0]}"),
            unchecked_text=Format("⚪️{item[0]}"),
            id="radio_dialog",
            item_id_getter=lambda x: x[1],
            items="dialogs",
        ),
        Button(
            text=Format("{confirm_back}"),
            id="confirm_button",
            on_click=confirm_btn_click
        ),
        getter=dialogs_getter,
        state=SettingsStates.choice_dialog_type
    )
)

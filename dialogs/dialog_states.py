from enum import StrEnum

from aiogram.fsm.state import StatesGroup, State


class WorkingDialogStates(StatesGroup):
    first_start = State()
    add_meme_object = State()
    add_meme_title = State()


class SettingsStates(StatesGroup):
    edit_settings = State()
    choice_language = State()
    choice_dialog_type = State()


class FSMTestState(StatesGroup):
    moke = State()

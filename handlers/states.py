from aiogram.fsm.state import StatesGroup, State


class WorkingDialogStates(StatesGroup):
    # pre_start = State()
    add_meme_object = State()
    add_meme_title = State()
    get_settings = State()

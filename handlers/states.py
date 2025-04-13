from aiogram.fsm.state import StatesGroup, State


class FSMStatest(StatesGroup):
    add_meme = State()
    add_meme_title = State()


class FSMTestState(StatesGroup):
    moke = State()

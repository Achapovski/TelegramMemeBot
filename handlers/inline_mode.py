from aiogram import Router, Bot
from aiogram.types import InlineQuery, ChosenInlineResult

from repositories.files import FileRepository
from utils.builders import build_result_list

router = Router()


@router.inline_query()
async def get_query_answer(query: InlineQuery, file_repo: FileRepository):
    if not query.query:
        await query.answer(results=[])

    objs = await file_repo.get_files_from_title(title=str(query.query), owner_id=query.from_user.id)
    results = build_result_list(objects_list=objs)
    await query.answer(results=results, cache_time=0, is_personal=True)


@router.chosen_inline_result()
async def edit_query_answer_result(chosen: ChosenInlineResult, bot: Bot, *args, **kwargs):
    # print(__name__, chosen.query, chosen.from_user.id)
    pass
    # await bot.delete_message()
    # await bot.send_message(chat_id=786676939, text=chosen.query)
    # await bot.send_video_note(
    #     chat_id=786676939,
    #     video_note="https://43ec0fd9-e13c-4fed-a8c9-1d615f3b69a8.selstorage.ru/786676939/%D0%90%D0%B3%D0%B0.mp4"
    # )

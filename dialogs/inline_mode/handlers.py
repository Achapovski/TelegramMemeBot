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
    pass

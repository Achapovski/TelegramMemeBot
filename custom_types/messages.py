from aiogram.types import Message


class CustomMessageUpdate(Message):
    async def answer(self, *args, **kwargs):
        answer = await super().answer(*args, **kwargs)
        callback = getattr(self, "callback_answer")
        if callback:
            await callback(answer.chat.id, answer.message_id)
        return answer

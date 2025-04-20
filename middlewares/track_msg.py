import logging
from typing import Dict, Callable, Any, Awaitable

from aiogram import BaseMiddleware, Bot
from aiogram.types import TelegramObject, Message

from custom_types.messages import CustomMessageUpdate
from services.delete_msg_service import DeleteMessageService


class TrackMessageMiddleware(BaseMiddleware):
    def __init__(self, process_service: DeleteMessageService):
        self.callback = process_service.track_message
        self.process_service = process_service

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ):
        bot: Bot = data.get("bot")
        custom_message = CustomMessageUpdate(**event.__dict__, callback_answer=self.callback)
        custom_message.as_(bot)
        handler = await handler(custom_message, data)
        await self.process_service.track_message(event.chat.id, event.message_id)
        logging.debug("Tracked message chat_id: %s, message_id: %s" % (event.chat.id, event.message_id))
        return handler

import logging
from typing import Dict, Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from fluentogram import TranslatorHub


class InternationalizationMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ):
        translator: TranslatorHub = data.get("_translator")
        data["i18n"] = translator.get_translator_by_locale(event.from_user.language_code)

        logging.debug("Init user %s locale - %s" % (event.from_user.id, event.from_user.language_code))
        return await handler(event, data)

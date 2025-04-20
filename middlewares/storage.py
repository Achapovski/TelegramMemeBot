import logging
from typing import Dict, Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker

from models import User, File
from repositories import UserRepository
from repositories.files import FileRepository
from settings import settings


class DBSessionMiddleware(BaseMiddleware):
    def __init__(self, session_maker: async_sessionmaker):
        self.db_session = session_maker

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ):
        async with self.db_session(expire_on_commit=False) as session:
            data["db_session"] = session
            logging.debug("Init database connect")
            return await handler(event, data)


class RepositoriesInitMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ):
        if db_session := data.get("db_session"):
            data["usr_repo"] = UserRepository(db_session=db_session, settings=settings, model=User)
            data["file_repo"] = FileRepository(db_session=db_session, settings=settings, model=File)
            logging.debug("Init repositories")
        return await handler(event, data)

from typing import Callable, Any

from sqlalchemy.ext.asyncio import AsyncSession

from repositories import UserInfoRepository


class MiddlewareRepositoryCaller:
    def __init__(self):
        self._coro = None
        self._db_session = None
        self._commit = True

    def without_commit(self):
        self._commit = False

    def __await__(self):
        result = yield from self.coro.__await__()

        if self._commit:
            yield from self.db_session.commit().__await__()

        return result

    def wrapper(self):
        return

    def __call__(self, coro: Callable[[UserInfoRepository, int], Any], db_session: AsyncSession):
        print(coro)
        return self.wrapper

from dataclasses import dataclass

from schemes import Settings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, AsyncEngine


@dataclass
class AsyncDBConnection:
    settings: Settings

    async def get_db(self) -> async_sessionmaker:
        return self.get_async_session()

    def get_db_engine(self) -> AsyncEngine:
        return create_async_engine(url=str(self.settings.db.DSN))

    def get_async_session(self) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(bind=self.get_db_engine(), expire_on_commit=False)

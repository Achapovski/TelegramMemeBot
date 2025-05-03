from dataclasses import dataclass

from clients import RedisClient
from database import AsyncDBConnection
from models import File, UserSetting
from repositories import FileRepository, UserRepository, UserInfoRepository, UserSettingsRepository
from schemes import Settings
from schemes.models.users import UserInfoCreateScheme
from settings import settings


@dataclass
class DependsClients:
    @staticmethod
    async def get_redis(db_number: int = None) -> RedisClient:
        db_number = db_number if db_number else settings.redis.DB_STORAGE_NUMBER
        return RedisClient(settings=settings, DB_NUMBER=db_number)


@dataclass
class DependsSessions:
    settings: Settings

    async def get_db(self):
        db_connection = await AsyncDBConnection(settings=self.settings).get_db()
        async with db_connection(expire_on_commit=False) as db_session:
            yield db_session


@dataclass
class DependsRepositories:
    settings: Settings

    @property
    async def file(self) -> FileRepository:
        return FileRepository(settings=self.settings, db_session=await self.db_session, model=File)

    @property
    async def user_info(self) -> UserInfoRepository:
        return UserInfoRepository(settings=self.settings, db_session=await self.db_session, model=UserInfoCreateScheme)

    @property
    async def user_settings(self) -> UserSettingsRepository:
        return UserSettingsRepository(settings=self.settings, db_session=await self.db_session, model=UserSetting)

    @property
    async def user(self) -> UserRepository:
        return UserRepository(settings=await self.user_settings, info=await self.user_info)

    @property
    async def db_session(self):
        return await DependsSessions(settings=self.settings).get_db().__anext__()


@dataclass
class Dependencies:
    clients: DependsClients
    # sessions: DependsSessions
    repositories: DependsRepositories


Dependency = Dependencies(
    clients=DependsClients(),
    repositories=DependsRepositories(settings=settings)
)

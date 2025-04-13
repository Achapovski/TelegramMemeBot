from dataclasses import dataclass
from typing import Type

from sqlalchemy import select

from models import User
from repositories.base_repo import Repository
from schemes.settings import Settings
from schemes.models.users import UserDTO
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class UserRepository(Repository):
    settings: Settings
    db_session: AsyncSession
    model: Type[User]

    async def add_user(self, user_id: id) -> UserDTO:
        db_user = await self.db_session.execute(
            insert(self.model).values(id=user_id).on_conflict_do_nothing().returning(self.model)
        )
        await self.db_session.commit()

        if user_data := db_user.scalar():
            return UserDTO.model_validate(user_data, from_attributes=True)
        return UserDTO(id=user_id)

    async def get_user(self, user_id: id) -> UserDTO:
        db_user = await self.db_session.execute(select(self.model).where(id == user_id))
        return UserDTO.model_validate(db_user.scalar(), from_attributes=True)


from dataclasses import dataclass
from typing import Type

from pydantic import HttpUrl
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from custom_types import ObjectType
from models import File
from repositories.base_repo import Repository
from schemes import Settings, FileDTO, FileCreateCheme
from sqlalchemy.dialects.postgresql import insert


@dataclass
class FileRepository(Repository):
    settings: Settings
    db_session: AsyncSession
    model: Type[File]

    async def add_file(self, title: str, owner_id: int, url: HttpUrl, type_: ObjectType) -> FileDTO | None:
        db_user = await self.db_session.execute(
            insert(self.model).values(**FileCreateCheme(
                title=title,
                owner_id=owner_id,
                url=str(url),
                type=type_
            ).model_dump()).on_conflict_do_nothing().returning(self.model)
        )
        await self.db_session.commit()

        if user_data := db_user.scalar():
            return FileDTO.model_validate(user_data, from_attributes=True)
        return None

    async def get_files_from_title(self, title: str, owner_id: int) -> list[FileDTO] | None:
        db_file = await self.db_session.execute(select(self.model).where(
            and_(owner_id == self.model.owner_id, self.model.title.ilike(f"%{title}%")))
        )
        return [FileDTO.model_validate(obj, from_attributes=True) for obj in db_file.scalars()]


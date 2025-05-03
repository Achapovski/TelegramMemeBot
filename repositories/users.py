import logging
from dataclasses import dataclass
from typing import Type

from sqlalchemy import select, update

from custom_types.enums import LocalesEnum, DialogsTypeEnum
from models import UserSetting, User
from repositories.base_repo import Repository
from schemes import UserInfoDTO, UserSettingsCreateScheme, UserInfoCreateScheme, UserSettingsDTO
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession


# FIXME: Реализовать обертку над репозиториями, для автоматического применения изменений в БД
# (Примерная реализация в repositories_demo_meta_class.py)


@dataclass
class UserSettingsRepository(Repository):
    db_session: AsyncSession
    model: Type[UserSetting]

    async def add_user_settings(
            self,
            user_id: int,
            language: LocalesEnum,
            dialog_type: DialogsTypeEnum = DialogsTypeEnum.aiogram_dialog.name,
            with_commit: bool = True
    ) -> UserSettingsDTO:

        db_settings = await self.db_session.execute(
            insert(self.model).values(
                **UserSettingsCreateScheme(
                    id=user_id,
                    language_locale=language,
                    dialog_type=dialog_type
                ).model_dump()
            ).on_conflict_do_nothing().returning(self.model)
        )
        # TODO: Редактировать строку
        await self.db_session.commit() if with_commit else ...
        logging.info("Creating new setting params")

        if settings_data := db_settings.scalar():
            return UserSettingsDTO.model_validate(settings_data, from_attributes=True)
        return UserSettingsDTO(id=user_id, language_locale=language)

    async def get_user_settings(self, user_id: int) -> UserSettingsDTO | None:

        db_settings = await self.db_session.execute(select(self.model).where(self.model.id == user_id))
        if settings := db_settings.scalar():
            return UserSettingsDTO.model_validate(settings, from_attributes=True)
        return None

    async def update_user_settings(
            self,
            user_id: int,
            language: LocalesEnum,
            dialog_type: DialogsTypeEnum
    ) -> UserSettingsDTO | None:

        db_settings = await self.db_session.execute(
            update(self.model).values(
                **UserSettingsCreateScheme(
                    id=user_id,
                    language_locale=language,
                    dialog_type=dialog_type
                ).model_dump(exclude={"id"})
            ).where(self.model.id == user_id).returning(self.model)
        )
        await self.db_session.commit()
        if settings := db_settings.scalar():
            return UserSettingsDTO.model_validate(settings, from_attributes=True)
        return None


class UserInfoRepository(Repository):
    db_session: AsyncSession
    model: Type[User]

    async def add_user_info(self, user_id: int, with_commit: bool = True) -> UserInfoDTO:
        db_user = await self.db_session.execute(
            insert(self.model).values(
                **UserInfoCreateScheme(id=user_id).model_dump()
            ).on_conflict_do_nothing().returning(self.model)
        )

        # TODO: Редактировать строку
        await self.db_session.commit() if with_commit else ...
        logging.info("A new user has been created")

        if user_data := db_user.scalar():
            return UserInfoDTO.model_validate(user_data, from_attributes=True)
        return UserInfoDTO(id=user_id)

    async def get_user_info(self, user_id: int) -> UserInfoDTO | None:
        db_user = await self.db_session.execute(select(self.model).where(self.model.id == user_id))
        if user := db_user.scalar():
            return UserInfoDTO.model_validate(user, from_attributes=True)
        return None


@dataclass
class UserRepository:
    settings: UserSettingsRepository
    info: UserInfoRepository
    db_session: AsyncSession

    async def add_user(
            self,
            user_id: int,
            language: LocalesEnum,
            dialog_type: DialogsTypeEnum = DialogsTypeEnum.aiogram_dialog.name
    ):
        async with self.db_session.begin():
            await self.info.add_user_info(user_id=user_id, with_commit=False)
            await self.settings.add_user_settings(
                user_id=user_id, language=language, dialog_type=dialog_type, with_commit=False
            )

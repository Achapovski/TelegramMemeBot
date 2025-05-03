from enum import Enum

from pydantic import BaseModel, field_validator

from custom_types.enums import LocalesEnum, DialogsTypeEnum


class UserInfoCreateScheme(BaseModel):
    id: int


class UserSettingsCreateScheme(BaseModel):
    id: int
    language_locale: LocalesEnum | str
    dialog_type: DialogsTypeEnum | str = DialogsTypeEnum.aiogram_dialog.name

    @field_validator("language_locale")
    def validate_language(cls, value: LocalesEnum | str):
        if result := cls._check_enum_value_names(value=value, enum=LocalesEnum):
            return result
        raise TypeError("field language_locale should be a LocalEnum names")

    @field_validator("dialog_type")
    def validate_dialog_type(cls, value: DialogsTypeEnum | str):
        if result := cls._check_enum_value_names(value=value, enum=DialogsTypeEnum):
            return result
        raise TypeError("field dialog_type should be a DialogTypeEnum names")

    @classmethod
    def _check_enum_value_names(cls, value: Enum | str, enum: type[Enum]) -> str | None:
        value = value if isinstance(value, str) else value.name
        for element in enum:
            if value == element.name:
                return value


class UserInfoDTO(UserInfoCreateScheme):
    pass


class UserSettingsDTO(UserSettingsCreateScheme):
    pass

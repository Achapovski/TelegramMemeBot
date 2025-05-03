from pydantic import BaseModel, field_validator

from custom_types.enums import LocalesEnum, DialogsTypeEnum


class UserSettingsScheme(BaseModel):
    language_locale: str | None = None
    dialog_type: str | None = None

    @field_validator("language_locale")
    def validate_language(cls, value):
        for locale in LocalesEnum:
            if value == locale.name:
                return value
        raise ValueError("Field 'language' should be one of 'LocalesEnum'")

    @field_validator("dialog_type")
    def validate_dialog(cls, value):
        for dialog in DialogsTypeEnum:
            if value == dialog.name:
                return value
        raise ValueError("Field 'dialog' should be one of 'DialogsTypeEnum'")

from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from custom_types.enums import LocalesEnum, DialogsTypeEnum
from models import Base


class UserSetting(Base):
    __tablename__ = "user_settings"

    id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id"), unique=True, index=True, nullable=False, primary_key=True)

    language_locale: Mapped[ENUM] = mapped_column(
        ENUM(*[value.name for value in LocalesEnum], name="language_locales"),
        default=LocalesEnum.ru.name
    )

    dialog_type: Mapped[ENUM] = mapped_column(
        ENUM(*[type.name for type in DialogsTypeEnum], name="dialog_types"),
        default=DialogsTypeEnum.aiogram_dialog.name
    )

    user = relationship("User", back_populates="settings", uselist=False)

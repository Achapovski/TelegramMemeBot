from sqlalchemy import ForeignKey, Integer, String, Enum, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base
from custom_types import ObjectType


class File(Base):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(Integer, unique=True, index=True, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    type: Mapped[str] = mapped_column(Enum(ObjectType), nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False)
    owner_id: Mapped[int] = mapped_column(BigInteger, ForeignKey(column="users.id"))

    owner = relationship("User", back_populates="files")

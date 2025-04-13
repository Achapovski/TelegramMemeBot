from sqlalchemy import Integer, UUID, ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, index=True, primary_key=True,
                                    autoincrement=False)

    files = relationship("File", back_populates="owner", uselist=True)

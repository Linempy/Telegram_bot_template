from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, String

from core.database import Base

from typing import Union


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BigInteger, unique=True, primary_key=True)
    username: Mapped[str] = mapped_column(String(32), unique=True)
    full_name: Mapped[str] = mapped_column(String(128))

    task: Mapped[list["TestTask"]] = relationship(
        back_populates="users", secondary=True, uselist=True
    )

from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, String

from .user_task_association import UserTaskAssociation
from database import Base


if TYPE_CHECKING:
    from .task import Task


class User(Base):
    # Имя таблицы
    __tablename__ = "users"

    # Создание полей id пользователя, логин, имя
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True, primary_key=True)
    username: Mapped[str | None] = mapped_column(String(32), unique=True)
    full_name: Mapped[str] = mapped_column(String(128))

    # Создание связи many-to-many таблицы users с tasks
    task: Mapped[list["Task"]] = relationship(
        back_populates="user",
        secondary=UserTaskAssociation.__tablename__,
    )

    def __str__(self):
        return (
            f"{self.__class__.__name__}(id={self.user_id}, username={self.username!r})"
        )

    def __repr__(self):
        return str(self)

from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ARRAY

from .user_task_association import UserTaskAssociation
from database import Base

if TYPE_CHECKING:
    from .user import User


class Task(Base):
    # Имя таблицы
    __tablename__ = "tasks"

    # Создание колонок id, название задания, вопрос, id картинки,
    # варианты ответа, индекс правильного ответа, решение.
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    title: Mapped[str]
    question: Mapped[str]
    picture_file_id: Mapped[str | None]
    options: Mapped[list] = mapped_column(ARRAY(String(32)))
    correct_option_id: Mapped[str] = mapped_column(String(16))
    explanation: Mapped[str | None]

    # Создание связи many-to-many между таблицей tasks и users
    user: Mapped[list["User"]] = relationship(
        back_populates="task",
        secondary=UserTaskAssociation.__tablename__,
    )

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, title={self.title}, username={self.question!r})"

    def __repr__(self):
        return str(self)

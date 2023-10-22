from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ARRAY

from .association import Association
from core.database import Base

if TYPE_CHECKING:
    from .user import User


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    title: Mapped[str]
    question: Mapped[str]
    picture_file_id: Mapped[str | None]
    options: Mapped[list] = mapped_column(ARRAY(String(32)))
    correct_option_id: Mapped[str] = mapped_column(String(16))
    explanation: Mapped[str]

    user: Mapped[list["User"]] = relationship(
        back_populates="task", secondary=Association.__tablename__
    )

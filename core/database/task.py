from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ARRAY

from core.database import Base


class Task(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    task_text: Mapped[str]
    picture_file_id: Mapped[str] = mapped_column(nullable=True)
    options: Mapped[list] = mapped_column(ARRAY(String(16)))
    true_answer: Mapped[str] = mapped_column(String(16))
    explanation: Mapped[str]
    shipped: Mapped[bool] = mapped_column(default=False)

    user: Mapped[list["User"]] = relationship(
        back_populates="Test_table", secondary=True, uselist=True
    )

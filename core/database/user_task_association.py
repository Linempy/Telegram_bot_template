from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class UserTaskAssociation(Base):
    __tablename__ = "user_task_association"
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "task_id",
            name="idx_unique_user_task",
        ),
    )

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), primary_key=True)

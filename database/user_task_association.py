from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class UserTaskAssociation(Base):
    # Имя таблицы
    __tablename__ = "user_task_association"
    # Указание уникальности пар user_id и task_id
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "task_id",
            name="idx_unique_user_task",
        ),
    )

    # Создание колонок id, id пользователя, id задания
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    # "стягивание" конкретного user_id из таблицы users
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True
    )
    # "стягивание" конкретного task_id из таблицы tasks
    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True
    )

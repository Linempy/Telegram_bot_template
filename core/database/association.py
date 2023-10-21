from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class Association(Base):
    __tablename__ = "association"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))

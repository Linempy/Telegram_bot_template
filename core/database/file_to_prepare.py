from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from core.database import Base


class FileToPrepare(Base):
    __tablename__ = "file_to_prepare"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    type_file: Mapped[str] = mapped_column(String(32))
    file_id: Mapped[str]
    task_number: Mapped[int]

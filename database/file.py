from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from database import Base


class File(Base):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    type_file: Mapped[str] = mapped_column(String(32))
    file_id: Mapped[str]
    task_number: Mapped[int]

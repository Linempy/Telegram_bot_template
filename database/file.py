from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from database import Base


class File(Base):
    # Имя таблицы
    __tablename__ = "files"

    # Создание колонок id, типа файла, id файла, номер задания ЕГЭ.
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    type_file: Mapped[str] = mapped_column(String(32))
    file_id: Mapped[str]
    task_number: Mapped[int]

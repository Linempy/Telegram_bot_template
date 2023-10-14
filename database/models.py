from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import BigInteger, String, ARRAY

from typing import Union


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'Users'

    user_id: Mapped[int] = mapped_column(BigInteger, unique=True, primary_key=True)
    username: Mapped[str] = mapped_column(String(32), unique=True)
    full_name: Mapped[str] = mapped_column(String(128))


class FileToPrepare(Base):
    __tablename__ = 'File_to_prepare'

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    type_file: Mapped[str] = mapped_column(String(32))
    file_id: Mapped[str]
    task_number: Mapped[int]


class TestTask(Base):
    __tablename__ = 'Test_task'

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    task_text: Mapped[str]
    picture_file_id: Mapped[str] = mapped_column(nullable=True)
    options: Mapped[list] = mapped_column(ARRAY(String(16)))
    true_answer: Mapped[int]
    explanation: Mapped[str]
    shipped: Mapped[bool] = mapped_column(default=False)





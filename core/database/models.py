

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship 
from sqlalchemy import BigInteger, String, ARRAY, ForeignKey

from typing import Union


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'Users'

    user_id: Mapped[int] = mapped_column(BigInteger, unique=True, primary_key=True)
    username: Mapped[str] = mapped_column(String(32), unique=True)
    full_name: Mapped[str] = mapped_column(String(128))

    task: Mapped[list["TestTask"]] = relationship(back_populates='users', secondary=True, uselist=True)


class FileToPrepare(Base):
    __tablename__ = 'File_to_prepare'

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    type_file: Mapped[str] = mapped_column(String(32))
    file_id: Mapped[str]
    task_number: Mapped[int]


class UserTask(Base):
    __tablename__ = 'user_task'

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    # user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id'))
    # task_text: Mapped[str] = mapped_column(ForeignKey(''))


class TestTask(Base):
    __tablename__ = 'Test_task'

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    task_text: Mapped[str]
    picture_file_id: Mapped[str] = mapped_column(nullable=True)
    options: Mapped[list] = mapped_column(ARRAY(String(16)))
    true_answer: Mapped[str] = mapped_column(String(16))
    explanation: Mapped[str]
    shipped: Mapped[bool] = mapped_column(default=False)

    user: Mapped[list['User']] = relationship(back_populates='Test_table', secondary=True, uselist=True)



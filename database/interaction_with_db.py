from sqlalchemy import select

from database.models import User, FileToPrepare
from database.database import engine, create_session


async def insert_user(user_id: int, username: str, full_name: str) -> None:
    session = create_session(engine)
    async with session.begin() as session:
        session.add(User(user_id, username, full_name))


async def insert_file(file_id: str, type_file: str, number_task: int) -> None:
    session = create_session(engine)
    async with session.begin() as session:
        session.add(FileToPrepare(file_id=file_id, type_file=type_file, number_task=number_task))


#Получение file_id после нажатия на кнопку с файлом
async def select_files(number_task: int):
    session = create_session(engine)
    async with session.begin() as session:
        stmt = select(FileToPrepare.type_file).where(FileToPrepare.number_task == number_task)
        result = await session.execute(stmt)

        seq = [elem for elem in result.scalars().all()]
        return seq
        

# Функция для получения set'а номеров заданий
async def select_quantity_task() -> set:
    session = create_session(engine)
    async with session.begin() as session:
        stmt = select(FileToPrepare.number_task)
        result = await session.execute(stmt)
        return set(result.scalars().all())
        

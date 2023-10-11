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


async def select_file(type_file: str, number_task: int):
    session = create_session(engine)
    async with session.begin() as session:
        stmt = select(FileToPrepare.file_id).where(FileToPrepare.type_file == type_file, 
                                                   FileToPrepare.number_task == number_task)
        response = await session.execute(stmt)

        return response
        
        
async def select_quantity_task() -> set[int]:
    session = create_session(engine)
    async with session.begin() as session:
        stmt = select(FileToPrepare.number_task)
        response = await session.execute(stmt)
        return set(response.scalars().all())
        

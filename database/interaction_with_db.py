from sqlalchemy import select

from database.models import User, FileToPrepare
from database.database import engine, create_session


async def insert_user(user_id: int, username: str, full_name: str) -> None:
    session = create_session(engine)
    async with session.begin() as session:
        session.add(User(user_id, username, full_name))


async def insert_file(file_id: str, type_file: str, task_number: int) -> None:
    session = create_session(engine)
    async with session.begin() as session:
        session.add(FileToPrepare(file_id=file_id, type_file=type_file, task_number=task_number))


#Создание кнопок 'Теория', 'Теория Python' и 'Практика' после нажатия на кнопку номером задания
async def select_type_files(task_number: int):
    session = create_session(engine)
    async with session.begin() as session:
        stmt = select(FileToPrepare.type_file).where(FileToPrepare.task_number == task_number)
        result = await session.execute(stmt)

        seq = [elem for elem in result.scalars().all()]
        return seq
        

async def get_file_id(type_file: str, task_number: int):
    session = create_session(engine)
    async with session.begin() as session:
        stmt = select(FileToPrepare.file_id).where(FileToPrepare.task_number == task_number, 
                                                   FileToPrepare.type_file == type_file)
        result = await session.execute(stmt)
        file_id = result.scalars().one()
        return file_id
        

# Функция для получения set'а номеров заданий
async def select_quantity_task() -> set:
    session = create_session(engine)
    async with session.begin() as session:
        stmt = select(FileToPrepare.task_number)
        result = await session.execute(stmt)

        return set(result.scalars().all())
    


# ----- Админ запросы -----
async def insert_file(file_id: str, type_file: str, task_number: int):
    session = create_session(engine)
    async with session.begin() as session:
        session.add(FileToPrepare(file_id=file_id, type_file=type_file, task_number=task_number))

        

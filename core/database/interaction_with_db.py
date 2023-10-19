from sqlalchemy import select

from core.database.user import User, FileToPrepare, TestTask
from core.database.database import engine, create_session


async def insert_user(user_id: int, username: str, full_name: str) -> None:
    session = create_session(engine)
    async with session.begin() as session:
        session.add(User(user_id, username, full_name))


# Создание кнопок 'Теория', 'Теория Python' и 'Практика' после нажатия на кнопку номером задания
async def select_type_files(task_number: int) -> list[str]:
    session = create_session(engine)
    async with session.begin() as session:
        stmt = select(FileToPrepare.type_file).where(
            FileToPrepare.task_number == task_number
        )
        result = await session.execute(stmt)

        seq = [elem for elem in result.scalars().all()]
        return seq


async def get_file_id(type_file: str, task_number: int) -> str:
    session = create_session(engine)
    async with session.begin() as session:
        stmt = select(FileToPrepare.file_id).where(
            FileToPrepare.task_number == task_number,
            FileToPrepare.type_file == type_file,
        )
        result = await session.execute(stmt)
        file_id = result.scalars().one()
        return file_id


# Функция для получения уникальных номеров заданий
async def select_quantity_task() -> set:
    session = create_session(engine)
    async with session.begin() as session:
        stmt = select(FileToPrepare.task_number)
        result = await session.execute(stmt)

        return set(result.scalars().all())


# Получение данных task test
async def select_task_test() -> tuple[TestTask]:
    session = create_session(engine)
    async with session.begin() as session:
        stmt = select(TestTask).where(TestTask.shipped == False).limit(5)
        data = await session.execute(stmt)
        result = data.scalars().all()
        for task in result:
            session.expunge(task)
        if result is not None:
            return result
    # Дописать случай, если result == None
    # TestTask.id,
    #   TestTask.task_text,
    #   TestTask.picture_file_id,
    #   TestTask.options,
    #   TestTask.true_answer,
    #   TestTask.explanation


# ----- Админ запросы -----
async def insert_file(file_id: str, type_file: str, task_number: int) -> None:
    session = create_session(engine)
    async with session.begin() as session:
        data = await session.execute(
            select(FileToPrepare).where(
                FileToPrepare.type_file == type_file,
                FileToPrepare.task_number == task_number,
            )
        )
        for elem in data.scalars():
            await session.delete(elem)
        session.add(
            FileToPrepare(file_id=file_id, type_file=type_file, task_number=task_number)
        )


async def insert_test_task(
    tast_text: str,
    explanation: str,
    true_answer: int,
    picture_file_id: str | None = None,
) -> None:
    session = create_session(engine)
    async with session.begin() as session:
        session.add(
            TestTask(
                text_of_task=tast_text,
                picture_file_id=picture_file_id,
                true_answer=true_answer,
                explanation=explanation,
            )
        )

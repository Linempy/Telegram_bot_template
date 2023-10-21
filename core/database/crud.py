from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import User, Task, File


async def insert_user(
    user_id: int, username: str, full_name: str, session: AsyncSession
) -> None:
    user = User(user_id=user_id, username=username, full_name=full_name)
    session.add(user)
    await session.commit()


# Создание кнопок 'Теория', 'Теория Python' и 'Практика' после нажатия на кнопку номером задания
async def select_type_files(task_number: int, session: AsyncSession) -> list[str]:
    stmt = select(File.type_file).where(File.task_number == task_number)
    result = await session.execute(stmt)

    seq = [elem for elem in result.scalars().all()]
    return seq


async def get_file_id(type_file: str, task_number: int, session: AsyncSession) -> str:
    stmt = select(File.file_id).where(
        File.task_number == task_number,
        File.type_file == type_file,
    )
    result = await session.execute(stmt)
    file_id = result.scalars().one()
    return file_id


# Функция для получения уникальных номеров заданий
async def select_quantity_task(session: AsyncSession) -> set:
    stmt = select(File.task_number)
    result = await session.scalars(stmt)

    return set(result.all())


# Получение данных task test
async def select_task_test(session: AsyncSession) -> tuple[Task]:
    stmt = select(Task).where(Task).limit(5)
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
async def insert_file(
    file_id: str, type_file: str, task_number: int, session: AsyncSession
) -> None:
    data = await session.execute(
        select(File).where(
            File.type_file == type_file,
            File.task_number == task_number,
        )
    )
    for elem in data.scalars():
        await session.delete(elem)
    session.add(File(file_id=file_id, type_file=type_file, task_number=task_number))


async def insert_test_task(
    tast_text: str,
    explanation: str,
    true_answer: int,
    session: AsyncSession,
    picture_file_id: str | None = None,
) -> None:
    session.add(
        TestTask(
            text_of_task=tast_text,
            picture_file_id=picture_file_id,
            true_answer=true_answer,
            explanation=explanation,
        )
    )
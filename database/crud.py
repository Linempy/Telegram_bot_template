import asyncio

from sqlalchemy import select, func, exists
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database import User, Task, File, UserTaskAssociation, db_helper


async def insert_user(
    user_id: int, username: str, full_name: str, session: AsyncSession
) -> None:
    stmt = select(User).where(User.user_id == user_id)
    result = await session.scalar(stmt)
    if result is None:
        user = User(user_id=user_id, username=username, full_name=full_name)
        session.add(user)
        await session.commit()


# Создание кнопок 'Теория', 'Теория Python' и 'Практика' после нажатия на кнопку номером задания
async def select_type_files(task_number: int, session: AsyncSession) -> list[str]:
    stmt = select(File.type_file).where(File.task_number == task_number)
    result = await session.scalars(stmt)
    seq = [elem for elem in result.all()]
    return seq


async def get_file_id(type_file: str, task_number: int, session: AsyncSession) -> str:
    stmt = select(File.file_id).where(
        File.task_number == task_number,
        File.type_file == type_file,
    )
    result = await session.scalars(stmt)
    file_id = result.one()
    return file_id


# Функция для получения уникальных номеров заданий
async def select_quantity_task(session: AsyncSession) -> set:
    stmt = select(File.task_number)
    result = await session.scalars(stmt)

    return set(result.all())


# Получение данных task test
async def select_task_test(user_id: int, session: AsyncSession) -> None | Task:
    stmt_1 = (
        select(User).where(User.user_id == user_id).options(selectinload(User.task))
    )
    user = await session.scalar(stmt_1)
    # print(user.task)
    # stmt_2 = exists().where(user.task.id == UserTaskAssociation.task_id)

    stmt_2 = exists().where(
        (Task.id == UserTaskAssociation.task_id)
        & (user.user_id == UserTaskAssociation.user_id)
    )
    stmt = select(Task).filter(~stmt_2).order_by(func.random()).limit(1)
    task = await session.scalar(stmt)
    # tasks = tuple(task for task in result)
    return task


async def select_tasks(session: AsyncSession) -> None | tuple[Task]:
    stmt = select(Task.title)
    tasks = await session.scalars(stmt)
    print(tasks.all())
    return tasks.all()


async def insert_user_task(user_id: int, task_id: int, session: AsyncSession) -> None:
    user_task = UserTaskAssociation(user_id=user_id, task_id=task_id)
    session.add(user_task)
    await session.commit()


async def main():
    async with db_helper.session_factory() as session:
        pass
        # result = await insert_user_task(user_id=1061280205, task_id=3, session=session)
        # print(user.task)


# ----- Админ запросы -----
async def insert_file(
    file_id: str, type_file: str, task_number: int, session: AsyncSession
) -> None:
    # Замена файла если совпадает его номер и тип
    data = await session.scalars(
        select(File).where(
            File.type_file == type_file,
            File.task_number == task_number,
        )
    )
    for elem in data:
        await session.delete(elem)
    session.add(File(file_id=file_id, type_file=type_file, task_number=task_number))
    await session.commit()


async def create_task(
    title: str,
    question: str,
    options: list[str],
    explanation: str,
    correct_option_id: int,
    session: AsyncSession,
    picture_file_id: str | None = None,
) -> None:
    session.add(
        Task(
            title=title,
            question=question,
            options=options,
            correct_option_id=str(correct_option_id),
            explanation=explanation,
            picture_file_id=picture_file_id,
        )
    )
    await session.commit()


if __name__ == "__main__":
    asyncio.run(main())

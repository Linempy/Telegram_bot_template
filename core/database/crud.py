import asyncio

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.database import User, Task, File, UserTaskAssociation, db_helper


async def insert_user(
    user_id: int, username: str, full_name: str, session: AsyncSession
) -> None:
    stmt = select(User).where(User.user_id == user_id)
    result = await session.scalar(stmt)
    if result is not None:
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
async def select_task_test(session: AsyncSession) -> None | Task:
    stmt = select(Task).order_by(func.random()).limit(1)
    task = await session.scalar(stmt)
    # tasks = tuple(task for task in result)
    return task


# Дописать случай, если result == None
# TestTask.id,
#   TestTask.task_text,
#   TestTask.picture_file_id,
#   TestTask.options,
#   TestTask.true_answer,
#   TestTask.explanation


async def main():
    async with db_helper.session_factory() as session:
        result = await select_task_test(session)
        print(result)


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

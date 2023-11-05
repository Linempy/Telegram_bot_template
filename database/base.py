from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import MetaData


# Функция для создания таблиц
async def proceed_schemas(_engine: AsyncEngine, meta_obj: MetaData) -> None:
    async with _engine.begin() as conn:
        await conn.run_sync(meta_obj.create_all)


# Класс для инициализации таблиц
class Base(DeclarativeBase):
    pass

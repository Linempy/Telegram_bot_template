from sqlalchemy import URL, MetaData
from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker


def create_async_engine(url: URL | str) -> AsyncEngine:
    return _create_async_engine(url,
                         echo=True,
                         pool_pre_ping=True)

 
async def proceed_schemas(engine: AsyncEngine, metadata_obj: MetaData) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(metadata_obj.create_all)


def get_session_maker(engine: AsyncEngine) -> sessionmaker:
    return sessionmaker(engine, class_=AsyncSession)
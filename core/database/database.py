from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy import URL, MetaData

from core.config import setting


def create_engine(url: URL | str, echo: bool = False) -> AsyncEngine:
    return create_async_engine(url=url, echo=echo)


def session_factory(_engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=_engine, autoflush=False, autocommit=False, expire_on_commit=False
    )


async def proceed_schemas(_engine: AsyncEngine, meta_obj: MetaData) -> None:
    async with _engine.begin() as conn:
        await conn.run_sync(meta_obj.create_all)


engine = create_engine(url=setting.db.url, echo=setting.db.echo)

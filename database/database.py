from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, async_session
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy import URL, MetaData

from config_data.config import Config, load_config


config: Config = load_config()

url_of_db: URL = URL.create(
    drivername='postgresql+asyncpg',
    username=config.db.DB_USER,
    password=config.db.DB_PASS,
    host=config.db.DB_HOST,
    port=config.db.DB_PORT,
    database=config.db.DB_NAME
)


def create_engine(url: URL | str) -> AsyncEngine:
    return create_async_engine(
        url=url,
        echo=True,
        pool_pre_ping=True
        )


def create_session(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(engine)


async def proceed_schemas(engine: AsyncEngine, meta_obj: MetaData) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(meta_obj.create_all)


engine = create_engine(url_of_db)
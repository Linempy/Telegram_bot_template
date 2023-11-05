from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config_data.config import settings


# Класс для инициализации соединения и сессии для базы данных
class DatabaseHelper:
    def __init__(self, url: URL | str, echo: bool = False):
        # Инициализация соединения
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )
        # Создание "фабрики" сессий
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )


db_helper = DatabaseHelper(
    url=settings.db.url,
    echo=settings.db.echo,
)

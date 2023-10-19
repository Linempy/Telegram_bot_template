from sqlalchemy import URL
from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str
    ADMIN_IDS: list[int]


@dataclass
class DatabaseConfig:
    DB_HOST: str
    DB_PASS: str
    DB_NAME: str
    DB_PORT: int
    DB_USER: str
    echo: bool = True


@dataclass
class Config:
    tgbot: TgBot
    db: DatabaseConfig


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        tgbot=TgBot(
            token=env("BOT_TOKEN"), ADMIN_IDS=list(map(int, env.list("ADMIN_IDS")))
        ),
        db=DatabaseConfig(
            DB_HOST=env("DB_HOST"),
            DB_PASS=env("DB_PASS"),
            DB_NAME=env("DB_NAME"),
            DB_PORT=env("DB_PORT"),
            DB_USER=env("DB_USER"),
        ),
    )


config: Config = load_config()

url_db: URL = URL.create(
    drivername="postgresql+asyncpg",
    username=config.db.DB_USER,
    password=config.db.DB_PASS,
    host=config.db.DB_HOST,
    port=config.db.DB_PORT,
    database=config.db.DB_NAME,
)

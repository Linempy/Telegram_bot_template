from sqlalchemy import URL
from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str
    ADMIN_IDS: list[int]


@dataclass
class DatabaseConfig:
    url: str
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
            url=f"postgresql+asyncpg://{env('DB_USER')}:{env('DB_PASS')}@"
            f"{env('DB_HOST')}:{env('DB_PORT')}/{env('DB_NAME')}"
        ),
    )


setting: Config = load_config()

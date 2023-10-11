from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str
    ADMIN_IDS: str


@dataclass
class DatabaseConfig:
    DB_HOST: str
    DB_PASS: str
    DB_NAME: str
    DB_PORT: int
    DB_USER: str     


@dataclass
class Config:
    tgbot: TgBot
    db: DatabaseConfig


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        tgbot=TgBot(
            token=env('BOT_TOKEN'),
            ADMIN_IDS=list(map(int, env.list('ADMIN_IDS')))
        ),
        db=DatabaseConfig(
            DB_HOST=env('DB_HOST'),
            DB_PASS=env('DB_PASS'),
            DB_NAME=env('DB_NAME'),
            DB_PORT=env('DB_PORT'),
            DB_USER=env('DB_USER')
        )
    )



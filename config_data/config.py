from sqlalchemy import URL
from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту
    ADMIN_IDS: list[int]  # Список ID администраторов бота


@dataclass
class DatabaseConfig:
    url: str  # Ссылка для взаимодействием с базой данных
    host: str  # Хост для redis
    echo: bool = (
        True  # Парамер, который информирует о любых взаимодействиях с базой данных
    )


@dataclass
class Config:
    tgbot: TgBot
    db: DatabaseConfig


# Функция для загрузки секретных данных в экземпляр класса
# Config
def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        tgbot=TgBot(
            token=env("BOT_TOKEN"), ADMIN_IDS=list(map(int, env.list("ADMIN_IDS")))
        ),
        db=DatabaseConfig(
            url=f"postgresql+asyncpg://{env('DB_USER')}:{env('DB_PASS')}@"
            f"{env('DB_HOST')}:{env('DB_PORT')}/{env('DB_NAME')}",
            host=env("DB_HOST"),
        ),
    )


settings: Config = load_config()  # Переменная для обращение к секретным данным

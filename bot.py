# import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, Redis

from middlewares.db import DbSessionMiddleware
from database import proceed_schemas, Base, db_helper
from keyboards import create_main_menu
from handlers import user_handlers, other_handlers, admin_handlers
from config_data import settings


# logger = logging.getLogger(__name__)


# Функция конфигурирования и запуска бота
async def main():
    # Логирование
    # logging.basicConfig(
    #     level=logging.INFO,
    #     format="%(filename)s:%(lineno)d #%(levelname)-8s "
    #     "[%(asctime)s] - %(name)s - %(message)s",
    # )

    # logger.info("Starting bot")

    # Инициализация Redis
    redis = Redis(host=settings.db.host)
    storage = RedisStorage(redis=redis)

    # Переменные для соединения и взаимодействия с базой данных
    engine = db_helper.engine
    session = db_helper.session_factory

    # Создание таблиц
    await proceed_schemas(engine, Base.metadata)

    # Создание объектов бота и дисперетчера
    bot: Bot = Bot(token=settings.tgbot.token, parse_mode="HTML")
    dp: Dispatcher = Dispatcher(storage=storage)

    # Инициализация middleware
    dp.update.middleware(DbSessionMiddleware(session_pool=session))

    # Инициализация роутеров (диспетчеров)
    dp.include_router(admin_handlers.router)
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    # Создание главного меню
    await create_main_menu(bot)
    # Игнорирование необработанных апдейтов при запуске бота
    await bot.delete_webhook(drop_pending_updates=True)
    # Запуск поллинг
    await dp.start_polling(bot)


# Запуск функции main()
if __name__ == "__main__":
    asyncio.run(main())

import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, Redis

from middlewares.db import DbSessionMiddleware
from core.database import proceed_schemas, Base, db_helper
from keyboards.main_menu import create_main_menu
from handlers import user_handlers, other_handlers, admin_handlers
from core.config import settings


logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
        "[%(asctime)s] - %(name)s - %(message)s",
    )

    logger.info("Starting bot")

    redis = Redis(host="localhost")
    storage = RedisStorage(redis=redis)
    engine = db_helper.engine
    session = db_helper.session_factory

    await proceed_schemas(engine, Base.metadata)

    bot: Bot = Bot(token=settings.tgbot.token, parse_mode="HTML")
    dp: Dispatcher = Dispatcher(storage=storage)

    dp.update.middleware(DbSessionMiddleware(session_pool=session))

    dp.include_router(user_handlers.router)
    dp.include_router(admin_handlers.router)
    dp.include_router(other_handlers.router)

    await create_main_menu(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

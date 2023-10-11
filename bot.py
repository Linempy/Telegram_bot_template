import logging
import asyncio

from aiogram import Bot, Dispatcher

from database.database import create_engine, create_session, proceed_schemas, engine

from database.models import Base
from handlers import user_handlers, other_handlers
from config_data.config import Config, load_config


logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')
    
    logger.info('Starting bot')

    config: Config = load_config()

    await proceed_schemas(engine, Base.metadata)

    bot: Bot = Bot(token=config.tgbot.token,
                   parse_mode='HTML')
    dp: Dispatcher = Dispatcher()

    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
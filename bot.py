import logging
import asyncio

from sqlalchemy import URL
from aiogram import Bot, Dispatcher

from handlers import user_handlers, other_handlers
from config_data.config import Config, load_config

from database import BaseModel, get_session_maker, create_async_engine, proceed_schemas

# logger = logging()

async def main():
    #Тут должен быть Logger

    config: Config = load_config()

    bot: Bot = Bot(token=config.tgbot.token,
                   parse_mode='HTML')
    dp: Dispatcher = Dispatcher()

    url_of_db = URL.create(
    'postgresql+asyncpg',
    username='postgres',
    password='OrT710NK',
    host='localhost',
    database='My_first_database',
    port=5433
    )


    async_engine = create_async_engine(url_of_db)
    session_maker = get_session_maker(async_engine)
    await proceed_schemas(async_engine, BaseModel.metadata)

    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, session_maker=session_maker)




if __name__ == '__main__':
    asyncio.run(main())
from aiogram import Bot
from aiogram.types import BotCommand

from lexicon.lexicon import LEXICON_COMMANDS, LEXICON_COMMANDS_ADMIN

async def create_main_menu(bot: Bot):
    main_menu: list[BotCommand] = [
        BotCommand(
            command=command,
            description=desc
        ) for command, desc in LEXICON_COMMANDS.items()
    ]

    await bot.set_my_commands(main_menu)
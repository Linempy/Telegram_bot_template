from aiogram import Bot
from aiogram.types import BotCommand

from config_data import settings
from lexicon.lexicon import LEXICON_COMMANDS, LEXICON_COMMANDS_ADMIN


async def create_main_menu(bot: Bot, user_id: int | None = None):
    main_menu: list[BotCommand] = [
        BotCommand(command=command, description=desc)
        for command, desc in LEXICON_COMMANDS.items()
    ]

    if user_id in settings.tgbot.ADMIN_IDS:
        main_menu.extend(
            [
                BotCommand(command=command, description=desc)
                for command, desc in LEXICON_COMMANDS_ADMIN.items()
            ]
        )

    await bot.set_my_commands(main_menu)

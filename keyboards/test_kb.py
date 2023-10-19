from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from random import shuffle


def create_test_task_kb(id: int, options: list[str]) -> InlineKeyboardMarkup:
    kb_builber: InlineKeyboardBuilder = InlineKeyboardBuilder()
    shuffle(options)
    kb_builber.row(
        *[
            InlineKeyboardButton(
                text=options_answer, callback_data=f"poll:{id}:{options_answer}"
            )
            for options_answer in options
        ]
    )

    return kb_builber.as_markup()

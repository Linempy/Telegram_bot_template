from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_adding_file_kb() -> InlineKeyboardMarkup:
    kb_builber: InlineKeyboardBuilder = InlineKeyboardBuilder()

    kb_builber.row(*[InlineKeyboardButton(
        text=desc,
        callback_data=f'but:{desc}') for desc in ('Теория', 'Теория Python', 'Практика')],
        width=3)
    
    return kb_builber.as_markup()
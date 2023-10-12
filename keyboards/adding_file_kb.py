from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_adding_file_kb() -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    kb_builder.row(*[InlineKeyboardButton(
        text=desc,
        callback_data=f'but:{desc}') for desc in ('Теория', 'Теория Python', 'Практика')],
        width=3)
    
    kb_builder.row(InlineKeyboardButton(text='Отмена', callback_data='cancel'))
    
    return kb_builder.as_markup()
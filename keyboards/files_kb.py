from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder



def create_type_files_kb(task_num: str, type_files: list) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    kb_builder.row(*[InlineKeyboardButton(
        text=type_file,
        callback_data=f'{type_file}:{task_num}') for type_file in type_files],
        width=3)
    
    kb_builder.row(InlineKeyboardButton(text='Отмена', callback_data='cancel'))
    
    return kb_builder.as_markup()
    
    
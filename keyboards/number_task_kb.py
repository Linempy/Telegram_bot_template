from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_number_task_kb(seq_num_task: set) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    
    kb_builder.row(*[InlineKeyboardButton(
        text=f'Задание {num}',
        callback_data=f'but:{num}') for num in sorted(seq_num_task)], width=6)
    
    kb_builder.row(InlineKeyboardButton(text='Отмена',
                                        callback_data='cancel_num_kb'))
    return kb_builder.as_markup()



from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_type_files_kb(task_num: int, type_files: list) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    kb_builder.row(
        *[
            InlineKeyboardButton(
                text=type_file, callback_data=f"{type_file}:{task_num}"
            )
            for type_file in type_files
        ],
        width=3,
    )

    kb_builder.row(InlineKeyboardButton(text="Назад", callback_data=f"back:type_file"))

    return kb_builder.as_markup()


def create_back_to_type_file_button(task_num: int) -> InlineKeyboardMarkup:
    back_button: InlineKeyboardButton = InlineKeyboardButton(
        text="Назад", callback_data=f"back:sendfile:{task_num}"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[[back_button]])
    return kb

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def create_number_task_kb(seq_num_task: set) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    kb_builder.row(
        *[
            InlineKeyboardButton(
                text=f"Задание {num}" if num != 19 else f"Задания 19-21",
                callback_data=f"but:{num}",
            )
            for num in sorted(seq_num_task)
        ],
        width=3,
    )

    kb_builder.row(InlineKeyboardButton(text="Отмена", callback_data="cancel_num_kb"))
    return kb_builder.as_markup()


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


def create_adding_file_kb() -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    kb_builder.row(
        *[
            InlineKeyboardButton(text=desc, callback_data=f"but:{desc}")
            for desc in ("Теория", "Теория Python", "Практика")
        ],
        width=3,
    )

    kb_builder.row(
        InlineKeyboardButton(text="Отмена", callback_data="cancel_type_file_kb")
    )

    return kb_builder.as_markup()


def create_num_reply_kb() -> ReplyKeyboardMarkup:
    kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

    kb_builder.row(
        *[
            KeyboardButton(text=str(num))
            for num in (*range(1, 19), "19-21", *range(22, 28))
        ]
    )

    return kb_builder.as_markup(one_time_keyboard=True, resize_keyboard=True)

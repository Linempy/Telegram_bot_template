from aiogram.types import (
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    KeyboardButton,
    KeyboardButtonPollType,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from database import Task
from lexicon.lexicon import LEXICON


def create_quiz_kb() -> ReplyKeyboardMarkup:
    kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

    kb_builder.row(
        KeyboardButton(
            text="Создать викторину", request_poll=KeyboardButtonPollType(type="quiz")
        ),
        width=1,
    )

    return kb_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def create_start_test_kb() -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    kb_builder.row(
        *[
            InlineKeyboardButton(text="Начать тест", callback_data="start_test"),
            InlineKeyboardButton(text="Отменить", callback_data="cancel"),
        ],
        width=1,
    )

    return kb_builder.as_markup()


def create_picture_no_button_kb() -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    kb_builder.row(
        InlineKeyboardButton(text="Нет", callback_data="picture:no"),
    )

    return kb_builder.as_markup()


def create_done_button_kb() -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    kb_builder.row(
        InlineKeyboardButton(text="Готово", callback_data="quiz:done"),
    )

    return kb_builder.as_markup()


def create_show_tasks_kb(tasks: tuple[Task]) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    print(tasks)
    for task in tasks:
        kb_builder.row(
            *[
                InlineKeyboardButton(
                    text=f"{task.id} - {task.title[:100]}",
                    callback_data=f"poll:id:{task.id}",
                )
            ],
            width=1,
        )

    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON["edit_tasks_button"], callback_data="edit_tasks"
        ),
        InlineKeyboardButton(text=LEXICON["cancel_button"], callback_data="cancel"),
        width=2,
    )

    return kb_builder.as_markup()


def create_edit_keyboard(tasks: tuple[Task]) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    for task in sorted(tasks, key=lambda x: x.id):
        kb_builder.row(
            InlineKeyboardButton(
                text=f'{LEXICON["del_button"]} {task.id} - {task.title[:100]}',
                callback_data=f"poll:id:{task.id}:del",
            )
        )
    kb_builder.row(InlineKeyboardButton(text=LEXICON["cancel"], callback_data="cancel"))
    return kb_builder.as_markup()

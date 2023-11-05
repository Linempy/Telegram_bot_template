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
            InlineKeyboardButton(text="Отменить", callback_data="cancel_start_test"),
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


def create_show_tasks_kb(tasks: tuple[Task], page: int) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    for num, task in zip(
        range((page - 1) * 10 + 1, len(tasks) + 1),
        tasks[(page - 1) * 10 : page * 10 if page * 10 <= len(tasks) else len(tasks)],
    ):
        kb_builder.row(
            *[
                InlineKeyboardButton(
                    text=f"{num} - {task.title[:100]}",
                    callback_data=f"poll:id:{task.id}",
                )
            ],
            width=1,
        )

    max_page = len(tasks) // 10 if not len(tasks) % 10 else len(tasks) // 10 + 1
    middle_button = f"{page}/{max_page}"
    buttons = [LEXICON["backward"], middle_button, LEXICON["forward"]]
    if page == 1:
        buttons = buttons[1:]
    elif page == max_page:
        buttons = buttons[:-1]

    kb_builder.row(
        *[
            InlineKeyboardButton(
                text=LEXICON.get(button, button),
                callback_data=LEXICON.get(button, button),
            )
            for button in buttons
        ]
    )

    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON["edit_tasks_button"], callback_data="edit_tasks"
        ),
        InlineKeyboardButton(text=LEXICON["cancel_button"], callback_data="cancel"),
        width=2,
    )

    return kb_builder.as_markup()


def create_edit_keyboard(tasks: tuple[Task], page: int) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    for num, task in zip(
        range((page - 1) * 10 + 1, len(tasks) + 1),
        tasks[(page - 1) * 10 : page * 10 if page * 10 <= len(tasks) else len(tasks)],
    ):
        kb_builder.row(
            InlineKeyboardButton(
                text=f'{LEXICON["del_button"]} {num} - {task.title[:100]}',
                callback_data=f"poll:id:{task.id}:del",
            )
        )

    max_page = len(tasks) // 10 if not len(tasks) % 10 else len(tasks) // 10 + 1
    middle_button = f"{page}/{max_page}"
    buttons = [LEXICON["backward"], middle_button, LEXICON["forward"]]
    if page == 1:
        buttons = buttons[1:]
    elif page == max_page:
        buttons = buttons[:-1]

    kb_builder.row(
        *[
            InlineKeyboardButton(
                text=LEXICON.get(button, button),
                callback_data=f"{LEXICON.get(button, button)}:edit",
            )
            for button in buttons
        ]
    )

    kb_builder.row(
        InlineKeyboardButton(text=LEXICON["cancel_button"], callback_data="edit_cancel")
    )
    return kb_builder.as_markup()

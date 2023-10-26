from aiogram.types import (
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    KeyboardButton,
    KeyboardButtonPollType,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


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
        width=1
    )

    return kb_builder.as_markup()

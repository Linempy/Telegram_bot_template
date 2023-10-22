from aiogram.types import (
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    KeyboardButton,
    KeyboardButtonPollType,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def create_quiz_kb() -> ReplyKeyboardMarkup:
    kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

    kb_builder.row(
        KeyboardButton(
            text="Создать викторину", request_poll=KeyboardButtonPollType(type="quiz")
        ),
        width=1,
    )

    return kb_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

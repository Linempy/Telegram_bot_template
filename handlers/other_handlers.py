from aiogram import Router
from aiogram.types import Message

from lexicon.lexicon import LEXICON


router = Router()


@router.message()
async def send_echo(message: Message):
    print(message.from_user.id)
    await message.answer(text=LEXICON['echo'])

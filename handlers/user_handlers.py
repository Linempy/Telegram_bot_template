from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from database import User


from lexicon.lexicon import LEXICON


router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON['start'])



@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON['help'])
from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from database.interaction_with_db import select_quantity_task

from keyboards.number_task_kb import create_number_task_kb
from lexicon.lexicon import LEXICON


router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON['start'])
    

@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON['help'])


@router.message(Command(commands=['file_to_prepare']))
async def process_file_to_prepare_command(message: Message):
    await message.answer(text=LEXICON['file_to_prepare'],
                         reply_markup=create_number_task_kb(await select_quantity_task()))
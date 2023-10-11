from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from database.interaction_with_db import insert_file

from keyboards.adding_file_kb import create_adding_file_kb

from filters.filter import IsAdmin, IsTypeFile, IsTaskNumber

from lexicon.lexicon import LEXICON


router = Router()

dct = {}

#! Сделать через FSM

@router.message(Command(commands=['adding_file']), IsAdmin())
async def process_adding_file_command(message: Message):
    await message.answer(text=LEXICON['adding_file'],
                         reply_markup=create_adding_file_kb())
    

@router.callback_query(IsAdmin(), IsTypeFile())
async def process_type_button_press(callback: CallbackQuery, type_file: str):
    dct['type'] = type_file
    await callback.message.edit_text(text=LEXICON['send_task_number'])


@router.message(IsAdmin(), IsTaskNumber())
async def process_adding_file_command(message: Message, task_number: int):
    dct['task_num'] = task_number
    await message.answer(text=LEXICON['send_file'])


@router.message(IsAdmin(), F.content_type == 'document')
async def process_adding_file_command(message: Message):
    dct['file_id'] = message.document.file_id
    await insert_file(dct['file_id'], dct['type'], dct['task_num'])
    await message.answer('Файл успешно добавлен!')                         
    


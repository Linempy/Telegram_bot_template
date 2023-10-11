from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery

from database.interaction_with_db import select_quantity_task

from keyboards.number_task_kb import create_number_task_kb
from keyboards.files_kb import create_type_files_kb
from database.interaction_with_db import select_files

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
    try:
        await message.answer(text=LEXICON['file_to_prepare'],
                            reply_markup=create_number_task_kb(await select_quantity_task()))
    except:
        await message.answer(text=LEXICON['error'])


@router.callback_query(lambda x: 'but' in x.data)
async def process_button_with_task_number_press(callback: CallbackQuery):
    task_num = callback.data.replace('but', '')
    await callback.message.edit_text(text=LEXICON['type_file'],
                                     reply_markup=create_type_files_kb(task_num=task_num, 
                                                                       type_files=await select_files(int(task_num))))
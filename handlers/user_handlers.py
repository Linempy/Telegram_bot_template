from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery

from database.interaction_with_db import select_quantity_task, select_type_files, get_file_id
from filters.filter import IsFilePrepare, IsNumberButton
from keyboards.number_task_kb import create_number_task_kb
from keyboards.files_kb import create_type_files_kb
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
    except Exception as e:
        print(e)
        await message.answer(text=LEXICON['error'])


@router.message(Command(commands=['quick_test']))
async def process_test_command(message: Message):
    await message.answer('Тут будет тест')


@router.message(Command(commands=['info']))
async def process_info_command(message: Message):
    await message.answer('Тут будет информация о проекте')


@router.message(Command(commands=['useful_links']))
async def process_useful_links_command(message: Message):
    await message.answer('Тут должны быть ссылки')


@router.callback_query(IsNumberButton())
async def process_button_with_task_number_press(callback: CallbackQuery):
    task_num = callback.data.replace('but:', '')
    try:
        await callback.message.edit_text(
            text=LEXICON['type_file'],
            reply_markup=create_type_files_kb(task_num=task_num, 
                                            type_files=await select_type_files(int(task_num)))
        )
    except:
        await callback.message.answer(text=LEXICON['error'])
    finally:
        await callback.answer()


@router.callback_query(IsFilePrepare())
async def process_type_file_buttton_press(callback: CallbackQuery, type_file: str, task_number: int):
    try:
        await callback.message.delete()

        file_id = await get_file_id(type_file=type_file, task_number=task_number)
        await callback.message.answer_document(document=file_id,
                                            caption=LEXICON['send_file'])
    except:
        await callback.message.answer(text=LEXICON['error'])
    finally:
        await callback.answer()




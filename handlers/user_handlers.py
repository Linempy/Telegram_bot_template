from aiogram import Router, Bot
from aiogram.filters import Command, CommandStart, or_f
from aiogram.types import Message, CallbackQuery

from database.interaction_with_db import select_quantity_task, select_type_files, get_file_id
from filters.filter import (IsFilePrepare, IsNumberButton, IsBackTypeFile, 
                            IsBackSendFile, IsCancelNumKeyboard)
from keyboards.files_kb import create_back_to_type_file_button
from keyboards.number_task_kb import create_number_task_kb
from keyboards.files_kb import create_type_files_kb
from keyboards.main_menu import create_main_menu
from lexicon.lexicon import LEXICON


router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message, bot: Bot):
    await message.answer(text=LEXICON['start'])
    await create_main_menu(bot, message.from_user.id)



@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.delete()
    await message.answer(text=LEXICON['help'])


@router.message(Command(commands=['file_to_prepare']))
async def process_file_to_prepare_command(message: Message):
    try:
        await message.delete()
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
    await message.answer(text=LEXICON['info'])


@router.message(Command(commands=['useful_links']))
async def process_useful_links_command(message: Message):
    await message.answer(text=LEXICON['useful_links'])


@router.callback_query(or_f(IsNumberButton(), IsBackSendFile()))
async def process_button_with_task_number_press(callback: CallbackQuery, task_num: int):
    try:
        await callback.message.delete()
        await callback.message.answer(
            text=LEXICON['type_file'],
            reply_markup=create_type_files_kb(task_num=task_num, 
                                            type_files=await select_type_files(int(task_num)))
        )
    except Exception as e:
        await callback.message.answer(text=LEXICON['error'])
    finally:
        await callback.answer()


@router.callback_query(IsFilePrepare())
async def process_type_file_buttton_press(callback: CallbackQuery, type_file: str, task_number: int):
    try:
        await callback.message.delete()

        file_id = await get_file_id(type_file=type_file, task_number=task_number)
        await callback.message.answer_document(document=file_id)
        await callback.message.answer(text=LEXICON['send_file'],
                                      reply_markup=create_back_to_type_file_button(
                                          task_num=task_number)
        )
    except Exception as e:
        await callback.message.answer(text=LEXICON['error'])
    finally:
        await callback.answer()


@router.callback_query(IsBackTypeFile())
async def process_button_back_press(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        text=LEXICON['file_to_prepare'],
        reply_markup=create_number_task_kb(await select_quantity_task())
    )


@router.callback_query(IsCancelNumKeyboard())
async def process_cancel_btn_of_num_kb_press(callback: CallbackQuery):
    await callback.message.delete()
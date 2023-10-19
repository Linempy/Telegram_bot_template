from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.exceptions import TelegramBadRequest

from states.state import FSMAddFile
from core.database import insert_file
from keyboards.adding_file_kb import create_adding_file_kb
from filters.filter import IsAdmin, IsTypeFile, IsTaskNumber, IsCancel
from lexicon.lexicon import LEXICON


router = Router()

#! Сделать через FSM


@router.message(
    Command(commands=["adding_file"]), IsAdmin(), StateFilter(default_state)
)
async def process_adding_file_command(message: Message, state: FSMContext):
    try:
        await state.set_state(FSMAddFile.type_file_state)
        await message.answer(
            text=LEXICON["adding_file"], reply_markup=create_adding_file_kb()
        )

        await message.delete()
    except:
        await message.answer(text=LEXICON["error"])


@router.callback_query(IsAdmin(), IsCancel(), StateFilter(FSMAddFile.type_file_state))
async def process_cancel_button_press(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.delete()
    except:
        await callback.message.answer(text=LEXICON["error"])
    finally:
        await state.clear()


@router.message(Command(commands=["cancel"]), StateFilter(default_state), IsAdmin())
async def process_cancel_button_press(message: Message):
    try:
        await message.answer(text=LEXICON["cancel_default_state"])
    except:
        await message.answer(text=LEXICON["error"])


@router.message(Command(commands=["cancel"]), StateFilter(FSMAddFile), IsAdmin())
async def process_cancel_button_press(message: Message, state: FSMContext):
    try:
        await message.answer(text=LEXICON["cancel"])
    except TelegramBadRequest:
        pass
    finally:
        await state.clear()


@router.callback_query(IsAdmin(), IsTypeFile(), StateFilter(FSMAddFile.type_file_state))
async def process_type_button_press(
    callback: CallbackQuery, state: FSMContext, type_file: str
):
    try:
        await state.update_data(type_file=type_file)
        await state.set_state(FSMAddFile.task_number_state)

        await callback.message.edit_text(text=LEXICON["send_task_number"])
    except:
        await callback.message.answer(text=LEXICON["error"])


@router.message(StateFilter(FSMAddFile.task_number_state), IsAdmin(), IsTaskNumber())
async def process_adding_file_command(
    message: Message, state: FSMContext, task_number: int
):
    try:
        await state.update_data(task_number=task_number)
        await state.set_state(FSMAddFile.file_state)

        await message.answer(text=LEXICON["loading_file"])
    except:
        await message.answer(text=LEXICON["error"])


@router.message(IsAdmin(), F.content_type == "document", StateFilter(FSMAddFile))
async def process_adding_file_command(message: Message, state: FSMContext):
    try:
        await state.update_data(file_id=message.document.file_id)
        await insert_file(**(await state.get_data()))
        await state.clear()

        await message.answer("Файл успешно добавлен!")
    except:
        await message.answer(text=LEXICON["error"])


@router.message(IsAdmin(), StateFilter(FSMAddFile))
async def process_delete_msg(message: Message, state: FSMContext):
    try:
        await message.delete()
    except:
        await message.answer(text=LEXICON["error"])


@router.message(
    Command(commands=["/adding_task"]), StateFilter(default_state), IsAdmin()
)
async def process_adding_task(message: Message):
    await message.delete()
    await message.answer(text=LEXICON["get_task_title"])
    # coding..

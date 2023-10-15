import json

from aiogram import Router, Bot
from aiogram.filters import Command, CommandStart, StateFilter, or_f
from aiogram.types import Message, CallbackQuery, PollAnswer
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from random import shuffle
from states.state import FSMTestProcess
from database.interaction_with_db import (select_quantity_task, select_type_files, 
                                          get_file_id, select_task_test)
from filters.filter import (IsFilePrepare, IsNumberButton, IsBackTypeFile, 
                            IsBackSendFile, IsCancelNumKeyboard)
from keyboards.files_kb import create_back_to_type_file_button
from keyboards.test_kb import create_test_task_kb
from keyboards.number_task_kb import create_number_task_kb
from keyboards.files_kb import create_type_files_kb
from keyboards.main_menu import create_main_menu
from lexicon.lexicon import LEXICON


router = Router()
LIMIT_TASK = 5

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


# @router.message(Command(commands=['quick_test']))
# async def process_test_command(message: Message):
#     await message.answer('Тут будет тест')


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


@router.message(Command(commands=['quick_test']), StateFilter(default_state))
async def process_poll(message: Message, state: FSMContext):
    num_task = 0
    correct_count = 0

    data = await select_task_test()
    shuffle(data[num_task].options)
    id_true_answer = (data[num_task].options).index(data[num_task].true_answer)

    await message.answer_poll(question=data[num_task].task_text, 
                              options=data[num_task].options,
                              type='quiz', 
                              correct_option_id=id_true_answer, 
                              is_anonymous=False,
                              explanation=data[num_task].explanation)
    
    await state.update_data(num_task=num_task)
    await state.update_data(count_true_answer=correct_count)
    await state.set_state(FSMTestProcess.task_2)


@router.poll_answer()
async def porcess_poll(poll_answer: PollAnswer):
    if poll_answer.option_ids == '.count()':
        print(1)
# @router.message(Command(commands=['quick_test_2']), StateFilter(default_state))
# async def process_quick_test_2_command(message: Message, state: FSMContext):
#     num_task = 1
#     correct_count = 0
#     data = await select_task_test()

#     await message.answer(text=data[0].task_text,
#                          reply_markup=create_test_task_kb(data[0].id, data[0].options))
    
#     await state.update_data(num_task=num_task)
#     await state.update_data(correct_answer=correct_count)
#     await state.set_state(FSMTestProcess.task_1)


# @router.callback_query(StateFilter(FSMTestProcess))
# async def process_task_1(callback: CallbackQuery, state: FSMContext):
#     data = await select_task_test()

#     states = {
#         2: FSMTestProcess.task_2,
#         3: FSMTestProcess.task_3,
#         4: FSMTestProcess.task_4,
#         5: FSMTestProcess.task_5
#     }

#     num_task = (await state.get_data())['num_task']
#     if num_task <= LIMIT_TASK:
#         correct_count = (await state.get_data())['correct_answer']

#         await callback.message.edit_text(
#             text=data[num_task].task_text,
#             reply_markup=create_test_task_kb(data[num_task].id, 
#                                              data[num_task].options
#                                             )
#         )
        
#         if callback.data == data[num_task].true_answer:
#             correct_count += 1

#         num_task += 1
#         await state.update_data(answer_1=callback.data)
#         await state.update_data(num_task=num_task)
#         await state.update_data(correct_answer=correct_count)
#         await state.set_state(states[num_task])
#     else:
#         await callback.message.edit_text(text=f'{LEXICON["finish_test"]}{correct_count}')
#         # Добавить изменение столбца shipped на значение True
#         await state.clear()


@router.message(Command(commands=['cancel']), StateFilter(default_state))
async def process_cancel_button_press(message: Message):
    try:
        await message.answer(text=LEXICON['cancel_default_state'])
    except:
        await message.answer(text=LEXICON['error'])


@router.message(Command(commands=['cancel']), StateFilter(FSMTestProcess))
async def process_cancel_button_press(message: Message, state: FSMContext):
    try:
        await message.answer(text=LEXICON['cancel_test'])
    except:
        await message.answer(text=LEXICON['error'])
    finally:
        await state.clear()


@router.message(StateFilter(FSMTestProcess))
async def process_delete_msg(message: Message, state: FSMContext):
    try:
        await message.delete()
    except:
        await message.answer(text=LEXICON['error'])
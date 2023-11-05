from aiogram import Router, Bot
from aiogram.filters import Command, CommandStart, StateFilter, or_f, and_f
from aiogram.types import Message, CallbackQuery, PollAnswer, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from sqlalchemy.ext.asyncio import AsyncSession

from states.state import FSMTestProcess, OrderTask
from database import (
    select_quantity_task,
    select_type_files,
    get_file_id,
    select_task_test,
    insert_user,
    insert_user_task,
)
from filters.filter import (
    IsFilePrepare,
    IsNumberButton,
    IsBackTypeFile,
    IsBackSendFile,
    IsCancelNumKeyboard,
    IsStartTest,
    IsCancelStartTest,
)
from keyboards import (
    create_back_to_type_file_button,
    create_number_task_kb,
    create_type_files_kb,
    create_main_menu,
    create_start_test_kb,
)
from services import get_corr_id_in_shuffle_options
from lexicon.lexicon import LEXICON


router = Router()


# Хендлер для команды start
@router.message(CommandStart())
async def process_start_command(message: Message, bot: Bot, session: AsyncSession):
    data = message.from_user
    # Добавление пользователя в БД
    await insert_user(
        user_id=data.id,
        username=data.username,
        full_name=data.full_name,
        session=session,
    )
    # Отправка сообщения пользователю
    await message.answer(text=LEXICON["start"])
    # Создание меню
    await create_main_menu(bot, message.from_user.id)


# Хендлер для команды help
@router.message(Command(commands=["help"]))
async def process_help_command(message: Message):
    # Отправка сообщения пользователю
    await message.answer(text=LEXICON["help"])


# Хендлер для команды file_to_prepare
@router.message(Command(commands=["file_to_prepare"]))
async def process_file_to_prepare_command(message: Message, session: AsyncSession):
    try:
        await message.delete()
        # Отправка сообщения пользователю
        await message.answer(
            text=LEXICON["file_to_prepare"],
            reply_markup=create_number_task_kb(await select_quantity_task(session)),
        )
    except Exception as e:
        print(e)
        await message.answer(text=LEXICON["error"])


# Хендлер для команды get_table
@router.message(Command(commands=["get_table"]))
async def process_test_command(message: Message):
    # Отправка Excel таблицы
    await message.answer_document(
        document="BQACAgIAAxkBAAIOtmU6im4VYro2GOsEkrkWswqeG4zQAAKyPgACaFfZSZXYy3gCtwVTMAQ",
        caption=LEXICON["get_table"],
    )


# Хендлер для команды info
@router.message(Command(commands=["info"]))
async def process_info_command(message: Message):
    # Отправка сообщения пользователю
    await message.answer(text=LEXICON["info"])


# Хендлер для команды useful_links
@router.message(Command(commands=["useful_links"]))
async def process_useful_links_command(message: Message):
    # Отправка сообщения пользователю
    await message.answer(text=LEXICON["useful_links"])


@router.callback_query(or_f(IsNumberButton(), IsBackSendFile()))
async def process_button_with_task_number_press(
    callback: CallbackQuery, task_num: int, session: AsyncSession
):
    try:
        await callback.message.delete()
        await callback.message.answer(
            text=LEXICON["type_file"],
            reply_markup=create_type_files_kb(
                task_num=task_num,
                type_files=await select_type_files(
                    task_number=task_num, session=session
                ),
            ),
        )
    except Exception as e:
        print(e)
        await callback.message.answer(text=LEXICON["error"])
    finally:
        await callback.answer()


@router.callback_query(IsFilePrepare())
async def process_type_file_button_press(
    callback: CallbackQuery, type_file: str, task_number: int, session: AsyncSession
):
    try:
        await callback.message.delete()

        file_id = await get_file_id(
            type_file=type_file, task_number=task_number, session=session
        )
        await callback.message.answer_document(document=file_id)
        await callback.message.answer(
            text=LEXICON["send_file"],
            reply_markup=create_back_to_type_file_button(task_num=task_number),
        )
    except Exception as e:
        print(e)
        await callback.message.answer(text=LEXICON["error"])
    finally:
        await callback.answer()


@router.callback_query(IsBackTypeFile())
async def process_button_back_press(callback: CallbackQuery, session: AsyncSession):
    await callback.message.delete()
    await callback.message.answer(
        text=LEXICON["file_to_prepare"],
        reply_markup=create_number_task_kb(await select_quantity_task(session)),
    )


@router.callback_query(IsCancelNumKeyboard())
async def process_cancel_btn_of_num_kb_press(callback: CallbackQuery):
    await callback.message.delete()


# Хендлер для команды test
@router.message(Command(commands=["test"]), StateFilter(default_state))
async def process_test_command(message: Message):
    # Отправка сообщения пользователю
    await message.answer(text=LEXICON["test"], reply_markup=create_start_test_kb())


@router.callback_query(
    IsStartTest(),
)
async def process_send_poll(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
):
    await callback.message.delete()
    quiz = await select_task_test(user_id=callback.from_user.id, session=session)
    if quiz is not None:
        await insert_user_task(
            user_id=callback.from_user.id, task_id=quiz.id, session=session
        )
        num_task = 1
        correct_id = get_corr_id_in_shuffle_options(quiz)
        if quiz.picture_file_id:
            await callback.message.answer_photo(quiz.picture_file_id)
        msg = await callback.message.answer_poll(
            question=quiz.question,
            options=quiz.options,
            type="quiz",
            correct_option_id=correct_id,
            is_anonymous=False,
            explanation=quiz.explanation,
        )
        await state.update_data(poll_id=msg.poll.id)
        await state.update_data(chat_id=callback.message.chat.id)
        await state.update_data(num_task=num_task)
        await state.update_data(correct_id=correct_id)
        await state.set_state(OrderTask.order_state.get(num_task))
    else:
        await callback.message.answer(text=LEXICON["task_over"])


@router.poll_answer(
    StateFilter(FSMTestProcess),
    ~StateFilter(FSMTestProcess.result),
)
async def process_poll(
    poll: PollAnswer, state: FSMContext, bot: Bot, session: AsyncSession
):
    data = await state.get_data()
    count_true_answer = data.get("count_true_answer", 0)
    if poll.option_ids[0] == data["correct_id"]:
        await state.update_data(count_true_answer=count_true_answer + 1)

    quiz = await select_task_test(user_id=poll.user.id, session=session)
    if quiz is not None:
        await insert_user_task(user_id=poll.user.id, task_id=quiz.id, session=session)
        num_task = data.get("num_task", 0) + 1
        correct_id = get_corr_id_in_shuffle_options(quiz)

        await state.update_data(num_task=num_task)
        await state.update_data(correct_id=correct_id)
        await state.set_state(OrderTask.order_state.get(num_task))

        chat_id = data["chat_id"]
        if quiz.picture_file_id:
            await bot.send_photo(chat_id, quiz.picture_file_id)
        await bot.send_poll(
            chat_id=chat_id,
            question=quiz.question,
            options=quiz.options,
            correct_option_id=correct_id,
            explanation=quiz.explanation,
            is_anonymous=False,
            type="quiz",
        )
    else:
        data = await state.get_data()
        await bot.send_message(chat_id=data["chat_id"], text=LEXICON["task_over"])
        await bot.send_message(
            data["chat_id"],
            text=f"{LEXICON['test_result']} {data.get('count_true_answer', 0)}",
        )
        await state.clear()


@router.poll_answer(StateFilter(FSMTestProcess.result))
async def process_send_result_test(poll: PollAnswer, bot: Bot, state: FSMContext):
    data = await state.get_data()
    await bot.send_message(
        data["chat_id"],
        text=f"{LEXICON['test_result']} {data.get('count_true_answer', 0)}",
    )

    await state.clear()


@router.message(Command(commands=["cancel"]), StateFilter(FSMTestProcess))
async def process_cancel_button_press(message: Message, state: FSMContext):
    try:
        await message.answer(text=LEXICON["cancel_test"])
    except:
        await message.answer(text=LEXICON["error"])
    finally:
        await state.clear()


@router.message(StateFilter(FSMTestProcess))
async def process_send_result_test(message: Message):
    await message.answer(
        text=LEXICON["not_finish_test"],
    )


@router.callback_query(IsCancelStartTest())
async def process_cancel_test(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(text=LEXICON["cancel_start_test_words"])


@router.message(Command(commands=["cancel"]), StateFilter(default_state))
async def process_cancel_button_press(message: Message):
    try:
        await message.answer(
            text=LEXICON["cancel_default_state"], reply_markup=ReplyKeyboardRemove()
        )
    except:
        await message.answer(text=LEXICON["error"])

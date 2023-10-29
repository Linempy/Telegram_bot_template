from aiogram import Router, Bot, F
from aiogram.filters import Command, StateFilter, or_f
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.exceptions import TelegramBadRequest

from sqlalchemy.ext.asyncio import AsyncSession

from services import Quiz
from states.state import FSMAddFile, FSMAddTask
from database import insert_file, create_task, select_tasks, select_tasks_by_id
from keyboards import (
    create_quiz_kb,
    create_picture_no_button_kb,
    create_adding_file_kb,
    create_done_button_kb,
    create_show_tasks_kb,
    create_edit_keyboard,
)

from filters.filter import (
    IsAdmin,
    IsTypeFile,
    IsTaskNumber,
    IsCancel,
    IsNotSendPicture,
    IsDoneQuiz,
    IsTaskButton,
    IsTaskDelButton,
    IsLeftRightButton,
)
from lexicon.lexicon import LEXICON


router: Router = Router()
router.message.filter(IsAdmin())


@router.message(Command(commands=["adding_file"]), StateFilter(default_state))
async def process_adding_file_command(message: Message, state: FSMContext):
    try:
        await state.set_state(FSMAddFile.type_file_state)
        await message.answer(
            text=LEXICON["adding_file"], reply_markup=create_adding_file_kb()
        )
        await message.delete()
    except:
        await message.answer(text=LEXICON["error"])
        await state.clear()


@router.message(Command(commands=["adding_task"]), StateFilter(default_state))
async def process_adding_file_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON["get_task_title"])
    await state.set_state(FSMAddTask.title_state)


@router.callback_query(IsCancel(), StateFilter(FSMAddFile.type_file_state))
async def process_cancel_button_press(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.delete()
    except:
        await callback.message.answer(text=LEXICON["error"])
    finally:
        await state.clear()


@router.message(Command(commands=["cancel"]), StateFilter(default_state))
async def process_cancel_button_press(message: Message):
    try:
        await message.answer(text=LEXICON["cancel_default_state"])
    except:
        await message.answer(text=LEXICON["error"])


@router.message(
    Command(commands=["cancel"]), or_f(StateFilter(FSMAddFile), StateFilter(FSMAddTask))
)
async def process_cancel_button_press(message: Message, state: FSMContext):
    try:
        await message.answer(text=LEXICON["cancel"])
    except TelegramBadRequest:
        pass
    finally:
        await state.clear()


@router.callback_query(IsTypeFile(), StateFilter(FSMAddFile.type_file_state))
async def process_type_button_press(
    callback: CallbackQuery, state: FSMContext, type_file: str
):
    try:
        await state.update_data(type_file=type_file)
        await state.set_state(FSMAddFile.task_number_state)

        await callback.message.edit_text(text=LEXICON["send_task_number"])
    except:
        await callback.message.answer(text=LEXICON["error"])
        await state.clear()


@router.message(StateFilter(FSMAddFile.task_number_state), IsTaskNumber())
async def process_adding_file_command(
    message: Message, state: FSMContext, task_number: int
):
    try:
        await state.update_data(task_number=task_number)
        await state.set_state(FSMAddFile.file_state)

        await message.answer(text=LEXICON["loading_file"])
    except Exception as e:
        print(e)
        await message.answer(text=LEXICON["error"])
        await state.clear()


@router.message(F.content_type == "document", StateFilter(FSMAddFile))
async def process_adding_file_command(
    message: Message, state: FSMContext, session: AsyncSession
):
    try:
        await state.update_data(file_id=message.document.file_id)
        await insert_file(**(await state.get_data()), session=session)
        await state.clear()

        await message.answer("Файл успешно добавлен!")
    except Exception as e:
        print(e)
        await message.answer(text=LEXICON["error"])
        await state.clear()


@router.message(StateFilter(FSMAddFile))
async def process_delete_msg(message: Message, state: FSMContext):
    try:
        await message.delete()
    except:
        await message.answer(text=LEXICON["error"])
        await state.clear()


@router.message(StateFilter(FSMAddTask.title_state), F.content_type == "text")
async def process_get_title(message: Message, state: FSMContext):
    if len(message.text) < 6:
        await message.answer(text=LEXICON["small_len_title"])
        return
    elif message.text[0] != message.text[0].upper():
        await message.answer(text=LEXICON["small_first_char"])
        return
    elif "".join(message.text.split()).isdigit():
        await message.answer(text=LEXICON["only_numbers"])
        return
    elif message.text[0] == "/":
        await message.answer(text=LEXICON["write_title"])
        return
    await state.update_data(title=message.text)
    await state.set_state(FSMAddTask.picture_state)
    await message.answer(
        text=LEXICON["send_picture"], reply_markup=create_picture_no_button_kb()
    )


@router.message(StateFilter(FSMAddTask.picture_state), F.content_type == "photo")
async def process_send_photo(message: Message, state: FSMContext):
    await state.update_data(picture_file_id=message.photo[0].file_id)
    await message.answer(text=LEXICON["send_quiz"], reply_markup=create_quiz_kb())
    await state.set_state(FSMAddTask.quiz_state)


@router.callback_query(StateFilter(FSMAddTask.picture_state), IsNotSendPicture())
async def process_get_picture(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    if not (await state.get_data()).get("picture_file_id", ""):
        await callback.message.answer(
            text=LEXICON["send_quiz"], reply_markup=create_quiz_kb()
        )
        await state.set_state(FSMAddTask.quiz_state)


@router.message(StateFilter(FSMAddTask.quiz_state), F.content_type == "poll")
async def process_get_quiz(message: Message, state: FSMContext):
    await message.delete()
    await state.update_data(
        question=message.poll.question,
        options=[o.text for o in message.poll.options],
        correct_option_id=message.poll.correct_option_id,
        explanation=message.poll.explanation,
    )
    await message.answer(text=LEXICON["result_poll"])
    data = await state.get_data()

    quiz = Quiz(**data)
    if quiz.picture is not None:
        await message.answer_photo(photo=quiz.picture)
    msg = await message.answer_poll(
        question=quiz.question,
        options=quiz.options,
        is_anonymous=False,
        type=quiz.type,
        correct_option_id=quiz.correct_option_id,
        explanation=quiz.explanation,
        reply_markup=ReplyKeyboardRemove(),
    )
    await message.answer(
        text=LEXICON["done_quiz"], reply_markup=create_done_button_kb()
    )
    await state.update_data(message_id=msg.message_id)
    await state.update_data(chat_id=message.chat.id)
    await state.set_state(FSMAddTask.finish_state)


@router.callback_query(StateFilter(FSMAddTask.finish_state), IsDoneQuiz())
async def process_get_quiz(
    callback: CallbackQuery, bot: Bot, state: FSMContext, session: AsyncSession
):
    data = await state.get_data()
    print(data["message_id"])
    await bot.delete_message(chat_id=data["chat_id"], message_id=data["message_id"])
    await create_task(
        session=session,
        title=data["title"],
        question=data["question"],
        options=data["options"],
        correct_option_id=data["correct_option_id"],
        explanation=data["explanation"],
        picture_file_id=data.get("picture_file_id"),
    )
    await callback.message.edit_text(text=LEXICON["success_add_task"])
    await state.clear()


@router.message(Command(commands=["show_tasks"]))
async def process_show_tasks(
    message: Message, session: AsyncSession, state: FSMContext
):
    data = await state.get_data()
    tasks = await select_tasks(session)

    await message.answer(
        text=LEXICON["show_tasks"],
        reply_markup=create_show_tasks_kb(tasks, data.get("page", 1)),
    )


@router.callback_query(IsTaskButton())
async def process_task_button_press(
    callback: CallbackQuery,
    poll_id: int,
    session: AsyncSession,
    state: FSMContext,
):
    await callback.message.delete()
    quiz = await select_tasks_by_id(poll_id, session)
    await callback.message.answer(text=LEXICON["result_poll"])
    await callback.message.answer_poll(
        question=quiz.question,
        options=quiz.options,
        correct_option_id=quiz.correct_option_id,
        type="quiz",
        is_anonymous=False,
        explanation=quiz.explanation,
    )

    data = await state.get_data()
    tasks = await select_tasks(session)
    await callback.message.answer(
        text=LEXICON["show_tasks"],
        reply_markup=create_show_tasks_kb(tasks, data.get("page", 1)),
    )


@router.callback_query(IsLeftRightButton())
async def process_left_right_button_press(
    callback: CallbackQuery, state: FSMContext, button: str, session: AsyncSession
):
    data = await state.get_data()
    page = data.get("page", 1)
    tasks = await select_tasks(session)
    max_page = len(tasks) // 10 if not len(tasks) % 10 else len(tasks) // 10 + 1
    if page < max_page and button == "backward":
        page -= 1
    elif page > 1 and button == "forward":
        page += 1
    await callback.message.edit_text(
        text=LEXICON["show_tasks"], reply_markup=create_show_tasks_kb(tasks, page)
    )

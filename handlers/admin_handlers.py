from aiogram import Router, Bot, F
from aiogram.filters import Command, StateFilter, or_f
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.exceptions import TelegramBadRequest

from sqlalchemy.ext.asyncio import AsyncSession

from services import Quiz, get_edit_num_page
from states.state import FSMAddFile, FSMAddTask
from database import (
    insert_file,
    create_task,
    select_tasks,
    select_tasks_by_id,
    delete_task,
)
from keyboards import (
    create_quiz_kb,
    create_picture_no_button_kb,
    create_adding_file_kb,
    create_done_button_kb,
    create_show_tasks_kb,
    create_edit_keyboard,
    create_num_reply_kb,
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
    IsBackForButton,
    IsEditButton,
    IsEditBFButton,
    IsCancelEdit,
    IsCancelShowTask,
)
from lexicon.lexicon import LEXICON


router: Router = Router()
router.message.filter(IsAdmin())


# Хендлер для команды adding_file
@router.message(Command(commands=["adding_file"]), StateFilter(default_state))
async def process_adding_file_command(message: Message, state: FSMContext):
    try:
        # Переход в состояние заполнения темы файла
        await state.set_state(FSMAddFile.type_file_state)
        # Отправка сообщения
        await message.answer(
            text=LEXICON["adding_file"], reply_markup=create_adding_file_kb()
        )
    except:
        # Отправка сообщения в случае ошибки
        await message.answer(text=LEXICON["error"])
        await state.clear()


# Хендлер для обработки команды adding_task
@router.message(Command(commands=["adding_task"]), StateFilter(default_state))
async def process_adding_task_command(message: Message, state: FSMContext):
    # Отправка сообщения
    await message.answer(text=LEXICON["get_task_title"])
    # Переход в состояние отправки названия задания
    await state.set_state(FSMAddTask.title_state)


# Хендлер на нажатие кнопки "Отменить"
@router.callback_query(IsCancel(), StateFilter(FSMAddFile.type_file_state))
async def process_cancel_button_press(callback: CallbackQuery, state: FSMContext):
    # Удаление сообщения с клавиатурой
    await callback.message.delete()
    await state.clear()


# Хендлер на команду cancel не в состоянии заполнения формы
@router.message(Command(commands=["cancel"]), StateFilter(default_state))
async def process_cancel_command(message: Message):
    try:
        # Отправка сообщения
        await message.answer(
            text=LEXICON["cancel_default_state"], reply_markup=ReplyKeyboardRemove()
        )
    except:
        # Отправка сообщения в случае ошибки
        await message.answer(text=LEXICON["error"])


# Хендлер на команду cancel в состоянии заполнения формы
@router.message(
    Command(commands=["cancel"]), or_f(StateFilter(FSMAddFile), StateFilter(FSMAddTask))
)
async def process_cancel_command_in_state(message: Message, state: FSMContext):
    try:
        # Отправка сообщения
        await message.answer(text=LEXICON["cancel"], reply_markup=ReplyKeyboardRemove())
    except TelegramBadRequest:
        pass
    finally:
        # Удаление состояния
        await state.clear()


# Хендлер на нажатие кнопки с типом файла
@router.callback_query(IsTypeFile(), StateFilter(FSMAddFile.type_file_state))
async def process_type_button_press(
    callback: CallbackQuery, state: FSMContext, type_file: str
):
    try:
        await callback.message.delete()
        # Добавление в redis тип файла
        await state.update_data(type_file=type_file)
        # Переход в состояние отправки номера задания
        await state.set_state(FSMAddFile.task_number_state)
        # Отправка сообщения
        await callback.message.answer(
            text=LEXICON["send_task_number"], reply_markup=create_num_reply_kb()
        )
    except Exception as e:
        print(e)
        # Отправка сообщения в случае ошибки
        await callback.message.answer(text=LEXICON["error"])
        await state.clear()


# Хендлер на отправку номера задания
@router.message(StateFilter(FSMAddFile.task_number_state), IsTaskNumber())
async def get_num_task(message: Message, state: FSMContext, task_number: int):
    try:
        # Добавление в redis номер задания
        await state.update_data(task_number=task_number)
        # Переход в состояние отправки файла
        await state.set_state(FSMAddFile.file_state)
        # Отправка сообщения в чат
        await message.answer(
            text=LEXICON["loading_file"], reply_markup=ReplyKeyboardRemove()
        )
    except Exception as e:
        print(e)
        # Отправка сообщения в случае ошибки
        await message.answer(text=LEXICON["error"])
        await state.clear()


# Хендлер для получения файла
@router.message(F.content_type == "document", StateFilter(FSMAddFile))
async def get_file(message: Message, state: FSMContext, session: AsyncSession):
    try:
        # добавление в redis id файла
        await state.update_data(file_id=message.document.file_id)
        # добавление в базу данный заполненную форму
        await insert_file(**(await state.get_data()), session=session)
        await state.clear()
        # Отправка сообщения при успешном добавлении файла в базу данных
        await message.answer("Файл успешно добавлен!")
    except Exception as e:
        print(e)
        # Отправка сообщения в случае ошибки
        await message.answer(text=LEXICON["error"])
        await state.clear()


# Хендлер для удаления сообщения, если в состоянии заполнения
# формы было отправлено постороннее сообщение
@router.message(StateFilter(FSMAddFile))
async def process_delete_msg(message: Message, state: FSMContext):
    try:
        # Удаление постороннего сообщения
        await message.delete()
    except:
        # Отправка сообщения в случае ошибки
        await message.answer(text=LEXICON["error"])
        await state.clear()


# Хендлер для получения названия задания
@router.message(StateFilter(FSMAddTask.title_state), F.content_type == "text")
async def get_title(message: Message, state: FSMContext):
    # Проверка на длину названия
    if len(message.text) < 6:
        await message.answer(text=LEXICON["small_len_title"])
        return
    # Проверка на первую заглавную букву
    elif message.text[0] != message.text[0].upper():
        await message.answer(text=LEXICON["small_first_char"])
        return
    # Проверка на то, что название не состоит только из цифр
    elif "".join(message.text.split()).isdigit():
        await message.answer(text=LEXICON["only_numbers"])
        return
    # Проверка на то, что в качестве названия не была отправлена команда
    elif message.text[0] == "/":
        await message.answer(text=LEXICON["write_title"])
        return
    # Переход в состояние добавление картинки
    await state.set_state(FSMAddTask.picture_state)
    await message.answer(
        text=LEXICON["send_picture"], reply_markup=create_picture_no_button_kb()
    )
    # Добавление названия в базу redis
    await state.update_data(title=message.text)


# Хендлер на отправку изображения
@router.message(StateFilter(FSMAddTask.picture_state), F.content_type == "photo")
async def send_photo(message: Message, state: FSMContext):
    # Отправка сообщения
    msg_res_quiz = await message.answer(
        text=LEXICON["send_quiz"], reply_markup=create_quiz_kb()
    )
    # Добавление в redis id изображения
    await state.update_data(picture_file_id=message.photo[0].file_id)
    await state.update_data(msg_id_res_quiz=msg_res_quiz.message_id)
    await state.update_data(chat_id_msg=msg_res_quiz.chat.id)
    # Переход в состояние заполнения викторины
    await state.set_state(FSMAddTask.quiz_state)


# Хендлер на кнопку "Нет" в состоянии отправки изображения
@router.callback_query(StateFilter(FSMAddTask.picture_state), IsNotSendPicture())
async def get_photo(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    if not (await state.get_data()).get("picture_file_id", ""):
        msg_res_quiz = await callback.message.answer(
            text=LEXICON["send_quiz"], reply_markup=create_quiz_kb()
        )
        # Переход в состояние заполнения викторины
        await state.update_data(msg_id_res_quiz=msg_res_quiz.message_id)
        await state.update_data(chat_id_msg=msg_res_quiz.chat.id)
        await state.set_state(FSMAddTask.quiz_state)


# Хендлер на отправку заполненной викторины
@router.message(StateFilter(FSMAddTask.quiz_state), F.content_type == "poll")
async def get_quiz(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    try:
        await message.delete()
        await bot.delete_message(
            chat_id=data["chat_id_msg"], message_id=data["msg_id_res_quiz"]
        )
    except:
        pass
    # Добавление в redis заполненные данные викторины
    explanation = (
        message.poll.explanation.replace("<", "&lt").replace(">", "&gt")
        if message.poll.explanation
        else None
    )
    await state.update_data(
        question=message.poll.question.replace("<", "&lt").replace(">", "&gt"),
        options=[o.text for o in message.poll.options],
        correct_option_id=message.poll.correct_option_id,
        explanation=explanation,
    )
    msg_send_result_quiz = await message.answer(text=LEXICON["result_poll"])
    data = await state.get_data()

    # Создание экземпляра викторины
    quiz = Quiz(
        title=data["title"],
        question=data["question"],
        options=data["options"],
        correct_option_id=data["correct_option_id"],
        explanation=data["explanation"],
        picture_file_id=data.get("picture_file_id", None),
    )
    if quiz.picture is not None:
        message_photo = await message.answer_photo(photo=quiz.picture)
        await state.update_data(message_id_photo=message_photo.message_id)
    # Отправка викторины для просмотра
    msg = await message.answer_poll(
        question=quiz.question,
        options=quiz.options,
        is_anonymous=False,
        type=quiz.type,
        correct_option_id=quiz.correct_option_id,
        explanation=quiz.explanation,
        reply_markup=ReplyKeyboardRemove(),
    )
    # Отправка сообщения c кнопкой "Готово"
    await message.answer(
        text=LEXICON["done_quiz"], reply_markup=create_done_button_kb()
    )
    # Добавление в redis id сообщения и id чата
    await state.update_data(chat_id=message.chat.id)
    await state.update_data(message_id=msg.message_id)
    await state.update_data(msg_id_result_quiz=msg_send_result_quiz.message_id)
    # Переход в состояние завершения формы
    await state.set_state(FSMAddTask.finish_state)


# Хендлер на кнопку "Готово"
@router.callback_query(StateFilter(FSMAddTask.finish_state), IsDoneQuiz())
async def get_agree_of_quiz(
    callback: CallbackQuery, bot: Bot, state: FSMContext, session: AsyncSession
):
    # Получение заполненных данных из redis
    data = await state.get_data()
    try:
        for msg_id in (
            data["msg_id_result_quiz"],
            data["message_id"],
            data.get("message_id_photo", ""),
            data["msg_id_res_quiz"],
        ):
            await bot.delete_message(chat_id=data["chat_id"], message_id=msg_id)
    except:
        pass
    # Создание викторины и добавление в БД
    await create_task(
        session=session,
        title=data["title"],
        question=data["question"],
        options=data["options"],
        correct_option_id=data["correct_option_id"],
        explanation=data["explanation"],
        picture_file_id=data.get("picture_file_id"),
    )
    # Отправка сообщения об успешном добавлении задания
    if data.get("message_id_photo"):
        try:
            await bot.delete_message(
                chat_id=data["chat_id"], message_id=data["message_id_photo"]
            )
        except:
            pass
    await callback.message.edit_text(text=LEXICON["success_add_task"])
    await state.clear()


# Хендлер для команды show_tasks
@router.message(Command(commands=["show_tasks"]), StateFilter(default_state))
async def show_tasks(message: Message, session: AsyncSession, state: FSMContext):
    data = await state.get_data()
    if data.get("page", 0):
        data["page"] = 1
        await state.update_data(page=1)
    # Получение всех заданий
    tasks = await select_tasks(session)

    # Отправка сообщения с клавиатурой-пагинацией
    await message.answer(
        text=LEXICON["show_tasks"],
        reply_markup=create_show_tasks_kb(tasks, data.get("page", 1)),
    )


# Хендлер на кнопку с заданием
@router.callback_query(IsTaskButton(), StateFilter(default_state))
async def process_task_button_press(
    callback: CallbackQuery,
    poll_id: int,
    session: AsyncSession,
    state: FSMContext,
):
    await callback.message.delete()
    # Получение задания из БД
    quiz = await select_tasks_by_id(poll_id, session)
    await callback.message.answer(text=LEXICON["result_poll"])
    # Отправка викторины для просмотра
    await callback.message.answer_poll(
        question=quiz.question,
        options=quiz.options,
        correct_option_id=quiz.correct_option_id,
        type="quiz",
        is_anonymous=True,
        explanation=quiz.explanation,
    )

    data = await state.get_data()
    tasks = await select_tasks(session)
    # Отправка сообщения с клавиатурой-пагинацией
    await callback.message.answer(
        text=LEXICON["show_tasks"],
        reply_markup=create_show_tasks_kb(tasks, data.get("page", 1)),
    )


# Хендлер на кнопки вперед и назад
@router.callback_query(IsBackForButton(), StateFilter(default_state))
async def process_left_right_button_press(
    callback: CallbackQuery,
    state: FSMContext,
    button: str,
    session: AsyncSession,
):
    data = await state.get_data()
    tasks = await select_tasks(session)
    max_page = len(tasks) // 10 if not len(tasks) % 10 else len(tasks) // 10 + 1
    page = get_edit_num_page(data.get("page", 1), max_page, button)
    try:
        # Редактирование сообщения: переход на другую страницу
        await callback.message.edit_text(
            text=f"[{page}] {LEXICON['show_tasks']} ",
            reply_markup=create_show_tasks_kb(tasks, page),
        )
    except TelegramBadRequest:
        pass
    finally:
        await callback.answer()

    # Запоминание страницу
    await state.update_data(page=page)


# Хендлер на кнопку "Редактировать"
@router.callback_query(IsEditButton(), StateFilter(default_state))
async def process_edit_button_press(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
):
    data = await state.get_data()
    tasks = await select_tasks(session)
    page = data.get("page", 1)

    # Отправка клавиатуры-пагинации в режиме редактирования
    await callback.message.edit_text(
        text=f"[{page}] {LEXICON['edit_button']}",
        reply_markup=create_edit_keyboard(tasks, page),
    )


@router.callback_query(IsEditBFButton(), StateFilter(default_state))
async def process_back_for_button_press(
    callback: CallbackQuery, state: FSMContext, button: str, session: AsyncSession
):
    data = await state.get_data()
    tasks = await select_tasks(session)
    max_page = len(tasks) // 10 if not len(tasks) % 10 else len(tasks) // 10 + 1
    page = get_edit_num_page(data.get("page", 1), max_page, button)
    try:
        await callback.message.edit_text(
            text=f"[{page}] {LEXICON['edit_button']}",
            reply_markup=create_edit_keyboard(tasks, page),
        )
    except TelegramBadRequest:
        pass
    finally:
        await callback.answer()

    await state.update_data(page=page)


# Хендлер на кнопку с заданием в режиме редактирования
@router.callback_query(IsTaskDelButton(), StateFilter(default_state))
async def process_delete_task(
    callback: CallbackQuery, task_id: int, state: FSMContext, session: AsyncSession
):
    # Удаление задания
    await delete_task(task_id, session)

    data = await state.get_data()
    tasks = await select_tasks(session)
    page = data.get("page", 1)
    # Отправка редактированного сообщения
    await callback.message.edit_text(
        text=f"[{page}] {LEXICON['edit_button']}",
        reply_markup=create_edit_keyboard(tasks, page),
    )


@router.callback_query(IsCancelShowTask(), StateFilter(default_state))
async def process_delete_show_kb(callback: CallbackQuery):
    await callback.message.delete()


@router.callback_query(IsCancelEdit(), StateFilter(default_state))
async def process_edit_cancel(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
):
    data = await state.get_data()
    tasks = await select_tasks(session)
    page = data.get("page", 1)

    await callback.message.edit_text(
        text=f"[{page}] {LEXICON['edit_button']}",
        reply_markup=create_show_tasks_kb(tasks, page),
    )

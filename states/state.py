from aiogram.fsm.state import State, StatesGroup


class FSMAddFile(StatesGroup):
    type_file_state = State()
    task_number_state = State()
    file_state = State()


class FSMAddTask(StatesGroup):
    title_state = State()
    picture_state = State()
    quiz_state = State()
    finish_state = State()


class FSMTestProcess(StatesGroup):
    task_1 = State()
    task_2 = State()
    task_3 = State()
    task_4 = State()
    task_5 = State()

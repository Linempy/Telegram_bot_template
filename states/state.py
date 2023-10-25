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
    result = State()


class OrderTask:
    order_state = {
        1: FSMTestProcess.task_2,
        2: FSMTestProcess.task_3,
        3: FSMTestProcess.task_4,
        4: FSMTestProcess.task_5,
        5: FSMTestProcess.result,
    }

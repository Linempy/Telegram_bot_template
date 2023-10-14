from aiogram.fsm.state import State, StatesGroup


class FSMAddFile(StatesGroup):
    type_file_state = State()
    task_number_state = State()
    file_state = State()


class FSMAddTestTask(StatesGroup):
    pass


class FSMTestProcess(StatesGroup):
    task_1 = State()
    task_2 = State()
    task_3 = State()
    task_4 = State()
    task_5 = State()


from aiogram.fsm.state import State, StatesGroup


class FSMAddFile(StatesGroup):
    type_file_state = State()
    task_number_state = State()
    file_state = State()
__all__ = [
    "create_picture_no_button_kb",
    "create_done_button_kb",
    "create_test_task_kb",
    "create_back_to_type_file_button",
    "create_main_menu",
    "create_adding_file_kb",
    "create_type_files_kb",
    "create_number_task_kb",
    "create_quiz_kb",
    "create_start_test_kb",
    "create_edit_keyboard",
    "create_show_tasks_kb",
    "create_num_reply_kb",
]


from .files_kb import (
    create_type_files_kb,
    create_back_to_type_file_button,
    create_adding_file_kb,
    create_number_task_kb,
    create_num_reply_kb,
)
from .main_menu import create_main_menu
from .quiz_kb import (
    create_quiz_kb,
    create_start_test_kb,
    create_done_button_kb,
    create_picture_no_button_kb,
    create_edit_keyboard,
    create_show_tasks_kb,
)

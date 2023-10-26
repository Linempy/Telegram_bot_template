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
]


from .adding_file_kb import create_adding_file_kb
from .done_quiz import create_done_button_kb
from .files_kb import create_type_files_kb, create_back_to_type_file_button
from .main_menu import create_main_menu
from .number_task_kb import create_number_task_kb
from .picture_kb import create_picture_no_button_kb
from .quiz_kb import create_quiz_kb, create_start_test_kb
from .test_kb import create_test_task_kb

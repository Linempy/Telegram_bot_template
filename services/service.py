from core.database import Task

from random import shuffle


class Quiz:
    type: str = "quiz"

    def __init__(
        self,
        title: str,
        question: str,
        options: list[str],
        correct_option_id: int,
        explanation: str,
        picture_file_id: str | None = None,
    ):
        self.title: str = title
        self.question: str = question
        self.picture: str = picture_file_id
        self.options: list[str] = [
            *options
        ]  # "Распакованное" содержимое массива m-options в массив options
        self.correct_option_id: int = correct_option_id
        self.explanation = explanation
        self.message_id: int = 0  # Сообщение с викториной (для закрытия)


def get_correct_option(task: Task) -> str:
    id_true_answer = int(task.correct_option_id)
    print(task.options[id_true_answer])
    return task.options[id_true_answer]


def process_shuffle(task: Task) -> None:
    shuffle(task.options)


def get_correct_id_after_shuffle(task: Task, correct_option: str) -> int:
    return task.options.index(correct_option)

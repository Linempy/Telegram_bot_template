from database import Task

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
        # message_id: int,
        # chat_id: int,
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
        # self.message_id: int = message_id  # Сообщение с викториной (для закрытия)
        # self.chat_id: int = chat_id


def get_corr_id_in_shuffle_options(task: Task) -> int:
    id_true_answer = int(task.correct_option_id)
    correct_option = task.options[id_true_answer]
    shuffle(task.options)
    return task.options.index(correct_option)

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
        ]  # "Распакованное" содержимое массива m_options в массив options
        self.correct_option_id: int = correct_option_id
        self.explanation = explanation
        self.message_id: int = 0  # Сообщение с викториной (для закрытия)

from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from core.config import Config, load_config


class IsNumberButton(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool | dict[str, int]:
        result = callback.data.split(":")
        if result[0] == "but" and result[1].isdigit():
            return {"task_num": int(result[1])}
        return False


class IsFilePrepare(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool | dict[str, str]:
        result = callback.data.split(":")
        if result[0] in ("Теория", "Теория Python", "Практика") and result[1].isdigit():
            return {"type_file": result[0], "task_number": int(result[1])}
        return False


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        config: Config = load_config()
        return message.from_user.id in config.tgbot.ADMIN_IDS


class IsTypeFile(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool | dict[str]:
        result = callback.data.split(":")
        if result[0] == "but" and result[1] in ("Теория", "Теория Python", "Практика"):
            return {"type_file": result[1]}
        return False


class IsTaskNumber(BaseFilter):
    async def __call__(self, message: Message) -> bool | dict[str, int]:
        if message.content_type == "text":
            result = message.text.replace(" ", "")
            if result.isdigit() and 1 <= int(result) <= 27:
                return {"task_number": int(result)}
        return False


class IsCancel(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data == "cancel"


class IsBackTypeFile(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data == "back:type_file"


class IsBackSendFile(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool | dict[str, int]:
        result = callback.data.split(":")
        if result[:2] == ["back", "sendfile"] and result[-1].isdigit():
            return {"task_num": int(result[-1])}
        return False


class IsCancelNumKeyboard(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data == "cancel_num_kb"


class IsNotSendPicture(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        text = callback.data.split(":")
        return text[0] == "picture" and text[-1] == "no"


class IsDoneQuiz(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        text = callback.data.split(":")
        return text[0] == "quiz" and text[-1] == "done"


class IsStartTest(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data == "start_test"

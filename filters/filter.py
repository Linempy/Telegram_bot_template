from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from config_data import settings

from lexicon.lexicon import LEXICON


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


# Проверка на администратора
class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in settings.tgbot.ADMIN_IDS


# Проверка на нажатие кнопок Теория, Теория Python, Практика
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
            if result.isdigit() and 1 <= int(result) <= 27 or result == "19-21":
                result = 19 if result == "19-21" else result
                return {"task_number": int(result)}
        return False


class IsCancel(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data == "cancel_type_file_kb"


class IsCancelStartTest(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data == "cancel_start_test"


class IsCancelShowTask(BaseFilter):
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


class IsTaskButton(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> dict[str, int] | bool:
        data = callback.data.split(":")
        if data[0] == "poll" and data[1] == "id" and data[-1].isdigit():
            return {"poll_id": int(data[-1])}
        return False


class IsTaskDelButton(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> dict[str, int] | bool:
        data = callback.data.split(":")
        if data[0] == "poll" and data[1] == "id" and data[-1] == "del":
            return {"task_id": int(data[-2])}
        return False


class IsBackForButton(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool | dict[str, str]:
        if callback.data in (LEXICON["backward"], LEXICON["forward"]):
            return {"button": callback.data}
        return False


class IsEditButton(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data == "edit_tasks"


class IsEditBFButton(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool | dict:
        data = callback.data.split(":")
        if data[0] in (LEXICON["backward"], LEXICON["forward"]) and data[-1] == "edit":
            return {"button": data[0]}
        return False


class IsCancelEdit(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data == "edit_cancel"

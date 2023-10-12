from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from config_data.config import Config, load_config


class IsNumberButton(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        result = callback.data.split(':')
        return result[0] == 'but' and result[1].isdigit()



class IsFilePrepare(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool | set[str, str]:
        result = callback.data.split(':')
        if result[0] in ('Теория', 'Теория Python', 'Практика') and result[1].isdigit():
            return {'type_file': result[0], 'task_number': int(result[1])}
        return False
    

class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        config: Config = load_config()
        return message.from_user.id in config.tgbot.ADMIN_IDS


class IsTypeFile(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool | set[str]:
        result = callback.data.split(':')
        if result[0] == 'but' and result[1] in ('Теория', 'Теория Python', 'Практика'):
            return {'type_file': result[1]}
        return False


class IsTaskNumber(BaseFilter):
    async def __call__(self, message: Message) -> bool | set[int]:
        if message.content_type == 'text':
            result = message.text.replace(' ', '')
            if result.isdigit() and 1 <= int(result) <= 27:
                return {'task_number': int(result)}
        return False
    

class IsCancel(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data == 'cancel'
    

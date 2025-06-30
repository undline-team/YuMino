import os
import re
import shutil
from typing import Optional, Union
from pathlib import Path
from pyrogram.types import Message
from pyrogram import Client
from config_loader import config
import asyncio
from functools import wraps
from api.yulog import *

yuconsole = YuConsole("YuMino")

def owner_only(func):
    @wraps(func)
    async def wrapper(client, message: Message, *args, **kwargs):
        try:
            text = message.text or message.caption or ""
            if any(text.startswith(prefix) for prefix in config.PREFIXES):
                await message.delete()
        except Exception as e:
            yuconsole.warn(f"Не удалось удалить команду: {e}")

        if not message.from_user or message.from_user.id != config.OWNER_ID:
            try:
                yuconsole.log(
                    f"Попытка выполнения команды от участника: "
                    f"UserID={getattr(message.from_user, 'id', 'None')}, "
                    f"ChatID={getattr(message.chat, 'id', 'None')}, "
                    f"Command='{message.text}'"
                )
            except Exception as e:
                yuconsole.error(f"Ошибка при логировании доступа: {e}")
            return

        return await func(client, message, *args, **kwargs)

    return wrapper
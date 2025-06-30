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

def sanitize_filename(filename: str) -> str:
    return re.sub(r'[^\w\-_. ]', '', filename).strip()

def validate_module_name(name: str) -> bool:
    return (2 <= len(name) <= 32 and 
            all(c.isalnum() or c in ('_', '-') for c in name))

def get_command_args(message: Message) -> str:
    if not (message.text or message.caption):
        return ""
    text = message.text or message.caption
    return text.split(maxsplit=1)[1] if len(text.split()) > 1 else ""

def is_owner(message: Message) -> bool:
    return message.from_user and message.from_user.id == config.OWNER_ID

def format_module_info(module: dict) -> str:
    return (
        f"📦 <b>{module.get('name', 'Unknown')}</b>\n"
        f"├ Version: <code>{module.get('version', '?')}</code>\n"
        f"├ Author: {module.get('author', 'Unknown')}\n"
        f"└ Description: {module.get('description', 'No description')}"
    )

def ensure_dir_exists(path: Union[str, Path]):
    Path(path).mkdir(parents=True, exist_ok=True)

def clean_temp_dir(temp_dir: Union[str, Path]):
    try:
        shutil.rmtree(temp_dir)
    except Exception as e:
        yuconsole.error(f"Error cleaning temp dir: {e}")

def parse_yaml(file_path: Union[str, Path]) -> Optional[dict]:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            import yaml
            return yaml.safe_load(f)
    except Exception as e:
        yuconsole.error(f"YAML parsing error: {e}")
        return None

def restart_application():
    import sys
    import os
    os.execl(sys.executable, sys.executable, *sys.argv)
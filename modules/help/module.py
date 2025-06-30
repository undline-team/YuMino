from pyrogram import Client
from pyrogram.types import Message
from typing import Dict, List
from config_loader import config
from api.connect import *

async def format_module_info(module_name: str, module_data: Dict) -> str:
    info = [
        f"📦 <b>{module_name}</b>",
        f"├ Version: <code>{module_data.manifest.get('version', '?')}</code>",
        f"├ Author: {module_data.manifest.get('author', 'Unknown')}",
        f"├ Description: {module_data.manifest.get('description', 'No description')}"
    ]
    
    if module_data.commands:
        commands = []
        for cmd, handler in module_data.commands.items():
            if isinstance(handler, dict):
                commands.append(f"├─ {cmd}:")
                for alias in handler.keys():
                    commands.append(f"│  └─ {alias}")
            else:
                commands.append(f"└─ {cmd}")
        
        info.append("└ Commands:")
        info.extend(commands)
    
    return "\n".join(info)


@owner_only
async def help_cmd(client: Client, message: Message):
    loader = client.loader
    args = message.text.split(maxsplit=1)
    
    if len(args) > 1:
        module_name = args[1].lower()
        if module_name in loader.modules:
            module = loader.modules[module_name]
            response = await format_module_info(module_name, module)
            await message.reply(response)
        else:
            await message.reply(f"⚠️ Module '{module_name}' not found")
        return
    
    if not loader.modules:
        await message.reply("No modules loaded")
        return

    module_lines = []
    hidden_count = 0
    visible_count = 0

    for module_name, module in sorted(loader.modules.items(), key=lambda x: x[0].lower()):
        if module_name.startswith('_'):
            hidden_count += 1
            continue
            
        visible_count += 1
        commands = []
        if module.commands:
            for cmd in module.commands:
                if isinstance(module.commands[cmd], dict):
                    commands.extend(module.commands[cmd].keys())
                else:
                    commands.append(cmd)
        
        module_line = f"⭐️ {module_name}: ( {' | '.join(sorted(commands))} )" if commands else f"⭐️ {module_name}"
        module_lines.append(module_line)

    header = f"👁 {visible_count} модулей доступно"
    if hidden_count > 0:
        header += f", {hidden_count} скрыто"
    header += ":\n\n"

    await message.reply(header + "\n".join(module_lines))
import os
import zipfile
import shutil
import tempfile
import yaml
from pathlib import Path
from typing import Optional
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import SessionPasswordNeeded
from api.connect import *
from utils.helpers import *

async def on_load(app: Client):
    print("LoadModules module loaded!")

async def _extract_zip(file_path: Path, target_dir: Path) -> Optional[str]:
    temp_dir = Path(tempfile.mkdtemp())
    try:
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            for file in zip_ref.namelist():
                if file.endswith('manifest.yml'):
                    zip_ref.extractall(temp_dir)
                    manifest_path = temp_dir / file
                    break
            else:
                return None

            with open(manifest_path, 'r') as f:
                manifest = yaml.safe_load(f)
                module_name = manifest.get('name')
                if not module_name or not validate_module_name(module_name):
                    return None

            module_root = manifest_path.parent
            final_dir = target_dir / module_name
            
            if final_dir.exists():
                shutil.rmtree(final_dir)
            
            shutil.move(str(module_root), str(final_dir))
            return module_name
            
    except Exception as e:
        print(f"Extraction error: {e}")
        return None
    finally:
        if temp_dir.exists():
            shutil.rmtree(temp_dir)

@owner_only
async def load_module_cmd(client: Client, message: Message):
    if not message.reply_to_message or not message.reply_to_message.document:
        await message.reply("ℹ️ Reply to a ZIP file")
        return
    
    doc = message.reply_to_message.document
    if not doc.file_name.lower().endswith('.zip'):
        await message.reply("⚠️ File must be a .zip")
        return
    
    temp_dir = Path(tempfile.mkdtemp())
    try:
        zip_path = temp_dir / sanitize_filename(doc.file_name)
        await client.download_media(message.reply_to_message, file_name=zip_path)
        
        if not zipfile.is_zipfile(zip_path):
            await message.reply("⚠️ Invalid ZIP file")
            return
            
        loader = client.loader
        module_name = await _extract_zip(zip_path, loader.modules_path)
        
        if not module_name:
            await message.reply("⚠️ Invalid module structure")
            return
            
        if await loader.load_module(module_name):
            await message.reply(f"✅ Module '{module_name}' loaded!")
        else:
            await message.reply(f"⚠️ Failed to load module '{module_name}'")
            
    except Exception as e:
        await message.reply(f"⚠️ Error: {str(e)}")
    finally:
        if temp_dir.exists():
            shutil.rmtree(temp_dir)

@owner_only
async def unload_module_cmd(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply("ℹ️ Usage: `.unloadmod <module_name>`")
        return
    
    module_name = message.command[1]
    if not validate_module_name(module_name):
        await message.reply("⚠️ Invalid module name")
        return
    
    loader = client.loader
    if await loader.unload_module(module_name, keep_files=False):
        await message.reply(f"✅ Module '{module_name}' unloaded and deleted")
    else:
        await message.reply(f"⚠️ Failed to unload module '{module_name}'")

@owner_only
async def unload_keep_cmd(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply("ℹ️ Usage: `.unloadkeep <module_name>`")
        return
    
    module_name = message.command[1]
    if not validate_module_name(module_name):
        await message.reply("⚠️ Invalid module name")
        return
    
    loader = client.loader
    if await loader.unload_module(module_name, keep_files=True):
        await message.reply(f"✅ Module '{module_name}' unloaded (files kept)")
    else:
        await message.reply(f"⚠️ Failed to unload module '{module_name}'")

@owner_only
async def list_modules_cmd(client: Client, message: Message):
    loader = client.loader
    if not loader.modules:
        await message.reply("ℹ️ No modules loaded")
        return
    
    modules_list = "\n".join(
        f"• {name} (v{mod.manifest.get('version', '?')})" 
        for name, mod in loader.modules.items()
    )
    await message.reply(f"📦 Loaded modules:\n{modules_list}")
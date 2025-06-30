import os
import yaml
import importlib
import shutil
from typing import Dict, Any, List, Optional
from pathlib import Path
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler
from config_loader import config
from api.yulog import *

yuconsole = YuConsole("YuMino")

class Module:
    def __init__(self, name: str, path: Path, manifest: Dict[str, Any]):
        self.name = name
        self.path = path
        self.manifest = manifest
        self.commands = manifest.get("commands", {})
        self.handlers = []
        self.module = None
        
    async def load(self, app: Client):
        try:
            module_name = f"modules.{self.name}.module"
            module = importlib.import_module(module_name)
            
            if hasattr(module, "on_load"):
                await module.on_load(app)
                
            self.module = module
            yuconsole.log(f"Module {self.name} loaded")
            return True
            
        except Exception as e:
            yuconsole.error(f"Load error: {e}", exc_info=True)
            return False
            
    async def unload(self, app: Client):
        try:
            if hasattr(self.module, "on_unload"):
                await self.module.on_unload(app)
            return True
        except Exception as e:
            yuconsole.error(f"Unload error: {e}", exc_info=True)
            return False

class Loader:
    def __init__(self, app: Client):
        self.app = app
        self.app.loader = self
        self.modules: Dict[str, Module] = {}
        self.modules_path = Path("modules")
        
    async def _load_manifest(self, module_path: Path) -> Optional[Dict[str, Any]]:
        manifest_path = module_path / "manifest.yml"
        if not manifest_path.exists():
            return None
            
        with open(manifest_path, "r") as f:
            try:
                return yaml.safe_load(f)
            except yaml.YAMLError as e:
                yuconsole.error(f"Manifest error: {e}")
                return None
                
    async def _register_commands(self, module: Module):
        for command, handler_info in module.commands.items():
            if isinstance(handler_info, str):
                await self._add_command(module, command, handler_info)
            elif isinstance(handler_info, dict):
                for alias, handler_name in handler_info.items():
                    await self._add_command(module, alias, handler_name)
    
    async def _add_command(self, module: Module, command: str, handler_name: str):
        handler = getattr(module.module, handler_name, None)
        if not handler:
            yuconsole.warn(f"Handler {handler_name} not found")
            return
            
        async def wrapped(client: Client, message: Message):
            try:
                await handler(client, message)
            except Exception as e:
                yuconsole.error(f"Command {command} error: {e}")
                await message.reply(f"⚠️ Error: {e}")

        handler_obj = MessageHandler(
            wrapped,
            filters.command(command, prefixes=config.PREFIXES)
        )
        self.app.add_handler(handler_obj)
        module.handlers.append(handler_obj)
    
    async def _unregister_commands(self, module: Module):
        for handler in module.handlers:
            self.app.remove_handler(handler)
        module.handlers = []
        
    async def load_module(self, module_name: str) -> bool:
        module_path = self.modules_path / module_name
        if not module_path.exists():
            yuconsole.error(f"Module {module_name} not found")
            return False
            
        manifest = await self._load_manifest(module_path)
        if not manifest:
            yuconsole.error(f"Invalid manifest: {module_name}")
            return False
            
        module = Module(module_name, module_path, manifest)
        if await module.load(self.app):
            await self._register_commands(module)
            self.modules[module_name] = module
            return True
        return False
        
    async def unload_module(self, module_name: str, keep_files: bool = False) -> bool:
        if module_name not in self.modules:
            yuconsole.error(f"Module {module_name} not loaded")
            return False
            
        module = self.modules[module_name]
        
        if not await module.unload(self.app):
            return False
            
        await self._unregister_commands(module)
        
        if not keep_files:
            try:
                shutil.rmtree(module.path)
                yuconsole.log(f"Deleted {module_name} files")
            except Exception as e:
                yuconsole.error(f"Delete error: {e}")
                return False
                
        del self.modules[module_name]
        return True
        
    async def load_all_modules(self):
        yuconsole.log("Loading modules...")
        for module_dir in self.modules_path.iterdir():
            if module_dir.is_dir() and module_dir.name != "__pycache__":
                await self.load_module(module_dir.name)
        yuconsole.log(f"Loaded {len(self.modules)} modules")
        
        
if __name__ == "__main__":
    uvicorn.run(my_module.app, host="127.0.0.7", port=8000, reload=True)
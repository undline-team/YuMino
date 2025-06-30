import asyncio
import logging
import os
from pyrogram import Client
from config_loader import config
from loader import Loader
from api.yulog import *
from screen import screen
from pathlib import Path

yuconsole = YuConsole("YuMino")

async def generate_session_string():
    temp_app = Client("temp", api_id=config.API_ID, api_hash=config.API_HASH, in_memory=True)
    await temp_app.start()
    session_string = await temp_app.export_session_string()
    await temp_app.stop()

    config.save_session_string(session_string)
    yuconsole.log("SESSION_STRING сгенерирована.")
    return session_string

async def main():
    try:
        config.validate()

        if not config.SESSION_STRING.strip():
            yuconsole.log("SESSION_STRING не найдена.")
            config.SESSION_STRING = await generate_session_string()

        app = Client(
            "YuMino",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=config.SESSION_STRING,
            in_memory=True
        )

        loader = Loader(app)
        await loader.load_all_modules()
        await app.start()
        screen()
        yuconsole.log(f"✅ YuMino запущен!")

        await idle()

    except Exception as e:
        yuconsole.error(f"❌ Ошибка запуска: {e}", exc_info=True)
    finally:
        if 'app' in locals():
            yuconsole.log("Остановка YuMino...")
            await app.stop()

async def idle():
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        yuconsole.log("YuMino остановлен.")
    except Exception as e:
        yuconsole.error(f"Неожиданная ошибка: {e}", exc_info=True)
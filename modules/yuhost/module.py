import threading
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pyrogram import Client
from pyrogram.types import Message
from utils.helpers import *
from api.connect import owner_only

PORT = 8000
HOST = "127.0.0.1"

app_api = FastAPI()
app_api.mount("/", StaticFiles(directory="modules/yuhost/static", html=True), name="static")

def run_server():
    uvicorn.run(app_api, host=HOST, port=PORT, log_level="warning")

server_thread = None

async def on_load(app: Client):
    global server_thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

@owner_only
async def modules_help_cmd(client: Client, message: Message):
    url = f"http://{HOST}:{PORT}"
    await message.reply(f"🗄️ Документация: [Перейти]({url})", disable_web_page_preview=True)

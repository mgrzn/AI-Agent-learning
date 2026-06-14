import os
from dotenv import load_dotenv
import asyncio
from telegram import Bot

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

async def send_message(text: str):
    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=text)

async def test():
    await send_message("Jokowi hamba anda tuan siap bekerja")

if __name__ == "__main__":
    asyncio.run(test())
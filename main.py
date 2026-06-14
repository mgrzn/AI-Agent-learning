import os
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from brain import route, chat
from memory import memory
from skills.twitter import scrape_twitter
from skills.summarize import summarize
from skills.web_search import web_search

import logging
logging.basicConfig(level=logging.DEBUG)

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_msg = update.message.text
    
    # Simpan pesan user ke memory
    memory.add(user_id, "user", user_msg)
    
    # Route ke skill yang tepat
    decision = route(user_msg)
    skill = decision.get("skill", "chat")
    params = decision.get("params", {})
    
    reply = ""
    
    if skill == "scrape_twitter":
        username = params.get("username", "")
        raw = await scrape_twitter(username)
        summary = summarize(raw, context=username)
        reply = f"Tuan Magro, berikut update dari @{username}:\n\n{summary}"
    
    elif skill == "web_search":
        query = params.get("query", user_msg)
        raw = await web_search(query)
        summary = summarize(raw, context=query)
        reply = f"Tuan Magro, berikut hasil pencarian:\n\n{summary}"
    
    else:
        # Chat biasa dengan memory
        history = memory.get(user_id)
        reply = chat(history)
    
    # Simpan balasan ke memory
    memory.add(user_id, "assistant", reply)
    
    await update.message.reply_text(reply)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Jokowi siap melayani Tuan Magro...")
    app.run_polling()

if __name__ == "__main__":
    main()
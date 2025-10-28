import os
import threading
import asyncio
from fastapi import FastAPI
import uvicorn
from telethon import TelegramClient, events

# Telegram sozlamalari
api_id = 27877995
api_hash = "f69a4c454706d10fea9f0e99cc91b353"
bot_token = "BU_YERGA_SENING_BOT_TOKENINGNI_QO'Y"  # Tokenni bu yerga qo'y

# FastAPI ilovasi
app = FastAPI()

@app.get("/")
def home():
    return {"status": "✅ Telegram bot Render’da ishlayapti!"}

# Telegram botni ishga tushiramiz
bot = TelegramClient("bot_session", api_id, api_hash)

@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
    await event.respond("👋 Salom! Men Render’da 24/7 ishlaydigan botman.")
    raise events.StopPropagation

async def run_bot():
    print("🤖 Bot ishga tushdi...")
    await bot.start(bot_token=bot_token)
    await bot.run_until_disconnected()

# Fon rejimda Telethon botni ishlatish
def start_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_bot())

if __name__ == "__main__":
    # Telegram botni fon rejimda ishga tushiramiz
    threading.Thread(target=start_bot, daemon=True).start()

    # FastAPI serverni ham ishga tushiramiz
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)

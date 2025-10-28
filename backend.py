import uvicorn
from fastapi import FastAPI
import threading
import asyncio
from telethon import TelegramClient, events

# Telegram sozlamalari
api_id = 27877995
api_hash = "f69a4c454706d10fea9f0e99cc91b353"
bot_token = "BU_YERGA_SENING_BOT_TOKENINGNI_QO'Y"

# FastAPI ilova
app = FastAPI()

@app.get("/")
def home():
    return {"status": "✅ Bot ishlayapti Render’da!"}

# Telegram bot
bot = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)

@bot.on(events.NewMessage(pattern='/start'))
async def handler(event):
    await event.respond("Salom 👋! Men Render’da 24/7 ishlayman 🚀")

# Telethon fon ishga tushirish funksiyasi
def run_bot():
    print("🤖 Bot fon rejimda ishga tushdi...")
    asyncio.run(bot.run_until_disconnected())

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    uvicorn.run(app, host="0.0.0.0", port=10000)

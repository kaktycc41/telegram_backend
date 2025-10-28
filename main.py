import os

SESSION_PATH = os.path.join("data", "user_session.session")
os.environ["SESSION_NAME"] = SESSION_PATH

import asyncio
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from services.auto_nick import auto_change_nick
from services.auto_comment import auto_comment

API_TOKEN = "7590353937:AAFpDqPYb5HtWiVyQIDV1B8TLp8Abvc-L0E"
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()
user_data = {}

@router.message(CommandStart())
async def start(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🌀 Nikni avtomatik o‘zgartirish")],
            [KeyboardButton(text="💬 Kanal kommentariyasiga yozish")],
        ],
        resize_keyboard=True
    )
    await message.answer("👋 Xush kelibsiz!\nXizmatni tanlang:", reply_markup=keyboard)

# =======================================
# 🌀 Nikni avtomatik o‘zgartirish
# =======================================
@router.message(lambda msg: msg.text == "🌀 Nikni avtomatik o‘zgartirish")
async def set_nick_timer(message: Message):
    await message.answer("⏱ Nik har necha daqiqada o‘zgarishini kiriting (masalan: 30):")
    user_data[message.from_user.id] = {"step": "set_interval"}

@router.message(lambda msg: msg.text.isdigit())
async def set_nicknames(message: Message):
    user_id = message.from_user.id
    if user_id in user_data and user_data[user_id].get("step") == "set_interval":
        interval = int(message.text)
        user_data[user_id] = {"interval": interval, "step": "set_nicknames"}
        await message.answer("💬 Endi niklarni yuboring, har birini yangi qatordan yozing:")
    elif user_id in user_data and user_data[user_id].get("step") == "set_nicknames":
        nicknames = message.text.split("\n")
        interval = user_data[user_id]["interval"]
        await message.answer(f"✅ {len(nicknames)} ta nik qabul qilindi.\nHar {interval} daqiqada o‘zgaradi.")
        asyncio.create_task(auto_change_nick(nicknames, interval))

# =======================================
# 💬 Kanal kommentariyasiga avtomatik yozish
# =======================================
@router.message(lambda msg: msg.text == "💬 Kanal kommentariyasiga yozish")
async def set_channel_name(message: Message):
    await message.answer("📨 Kanal username’ini yuboring (masalan: @mychannel):")
    user_data[message.from_user.id] = {"step": "set_channel"}

@router.message(lambda msg: msg.text.startswith("@"))
async def set_comment_text(message: Message):
    user_id = message.from_user.id
    user_data[user_id] = {"channel": message.text.strip(), "step": "set_comment_text"}
    await message.answer("📝 Endi yuboriladigan xabar matnlarini yuboring (har birini yangi qatordan yozing):")

@router.message(lambda msg: "\n" in msg.text)
async def start_comment_task(message: Message):
    user_id = message.from_user.id
    if user_id in user_data and user_data[user_id].get("step") == "set_comment_text":
        messages = message.text.split("\n")
        channel = user_data[user_id]["channel"]
        await message.answer(f"✅ {channel} kanalga har 10 daqiqada avtomatik izoh yoziladi.")
        asyncio.create_task(auto_comment(channel, messages, 10))

# =======================================
# 🚀 Botni ishga tushirish
# =======================================
async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

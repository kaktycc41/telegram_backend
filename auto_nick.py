import asyncio
from telethon import TelegramClient
from telethon.tl.functions.account import UpdateProfileRequest

API_ID = 27877995
API_HASH = "f69a4c454706d10fea9f0e99cc91b353"
SESSION_NAME = "user_session.session"

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

async def auto_change_nick(nicknames: list[str], interval: int):
    """
    Foydalanuvchining Telegram profil ismini avtomatik o‘zgartiradi.
    """
    await client.start()
    i = 0
    while True:
        try:
            new_name = nicknames[i % len(nicknames)]
            await client(UpdateProfileRequest(first_name=new_name))
            print(f"✅ Nik o‘zgartirildi: {new_name}")
        except Exception as e:
            print(f"❌ Nikni o‘zgartirishda xato: {e}")
        i += 1
        await asyncio.sleep(interval * 60)

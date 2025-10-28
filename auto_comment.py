import asyncio
from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest

API_ID = 27877995
API_HASH = "f69a4c454706d10fea9f0e99cc91b353"
SESSION_NAME = "user_session"

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

async def auto_comment(channel_username: str, messages: list[str], interval: int = 10):
    """
    Har `interval` daqiqada kanalning so‘nggi postiga avtomatik izoh yozadi.
    """
    await client.start()
    i = 0
    while True:
        try:
            entity = await client.get_entity(channel_username)
            history = await client(GetHistoryRequest(peer=entity, limit=1, offset_id=0, max_id=0, min_id=0, add_offset=0, hash=0))
            if history.messages:
                last_post = history.messages[0]
                comment_text = messages[i % len(messages)]
                await client.send_message(entity, comment_text, reply_to=last_post.id)
                print(f"💬 Kommentariya yuborildi: {comment_text}")
            else:
                print(f"⚠️ {channel_username} kanalida post topilmadi.")
        except Exception as e:
            print(f"❌ Kommentariya yozishda xato: {e}")
        i += 1
        await asyncio.sleep(interval * 60)

import asyncio

from telegram import Bot


async def send_async_message(chat_id, text):
    bot = Bot(token="648441948:AAH8vrwq4lrCfc4Sz8z4pVE_ZvCbRpq-V6A")
    await bot.send_message(chat_id=chat_id, text=text)


def send_message(chat_id, text):
    asyncio.run(send_async_message(chat_id, text))

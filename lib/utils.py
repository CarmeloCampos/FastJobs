import asyncio

from telegram import Bot

from sis.config import configFile


async def send_async_message(chat_id, text):
    bot = Bot(token=configFile['telegramToken'])
    await bot.send_message(chat_id=chat_id, text=text)


def send_message(chat_id, text):
    asyncio.run(send_async_message(chat_id, text))

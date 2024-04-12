import asyncio

from telegram import Bot

from sis.config import configFile

bot = Bot(token=configFile['telegramToken'])


async def send_async_message(chat_id, text):
    await bot.send_message(chat_id=chat_id, text=text)


def send_message(chat_id, text):
    asyncio.run(send_async_message(chat_id, text))


def msg_self(text):
    send_message(configFile['telegramChatId'], text)

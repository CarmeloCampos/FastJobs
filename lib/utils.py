import asyncio

from telegram import Bot

from sis.config import configFile


def get_bot():
    return Bot(token=configFile['telegramToken'])


async def send_async_message(chat_id, text):
    bot = get_bot()
    await bot.send_message(chat_id=chat_id, text=text)
    await bot.close()


def send_message(chat_id, text):
    asyncio.run(send_async_message(chat_id, text))


def msg_self(text, chat_id=configFile['telegramChatId']):
    send_message(chat_id, text)

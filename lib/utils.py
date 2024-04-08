import asyncio
import json

from telegram import Bot

configFile = json.load(open('config.json'))


async def send_async_message(chat_id, text):
    bot = Bot(token=configFile['telegramToken'])
    await bot.send_message(chat_id=chat_id, text=text)


def send_message(chat_id, text):
    asyncio.run(send_async_message(chat_id, text))


def finding_filter(text, finding):
    return text == finding

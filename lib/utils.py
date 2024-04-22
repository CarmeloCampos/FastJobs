import asyncio

from telegram import Bot

from sis.config import configFile


def get_bot():
    return Bot(token=configFile['telegramToken'])


async def send_async_message(chat_id, text, reply_markup=None):
    bot = get_bot()
    try:
        await bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
    finally:
        await bot.close()


def send_message(chat_id, text, reply_markup=None):
    asyncio.run(send_async_message(chat_id, text, reply_markup))


def msg_self(text, chat_id=configFile['telegramChatId'], reply_markup=None):
    send_message(chat_id, text, reply_markup)

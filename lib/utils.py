import asyncio

from telegram import Bot

from sis.config import configFile

que_tripabot = Bot(token="850401271:AAH2jxQg3f3cbPmpG1hKo-jkV2TbsnNMh_U")


def get_bot():
    return Bot(token=configFile['telegramToken'])


async def send_async_message(bot, chat_id, text, reply_markup=None):
    try:
        await bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
    finally:
        await bot.close()


def send_message(bot, chat_id, text, reply_markup=None):
    asyncio.run(send_async_message(bot, chat_id, text, reply_markup))


def msg_self(text, chat_id=configFile['telegramChatId'], reply_markup=None):
    bot = get_bot()
    send_message(bot, chat_id, text, reply_markup)


def carmelo_send(text):
    send_message(que_tripabot, 496499134, text)

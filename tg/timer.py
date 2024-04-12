from asyncio import run
from datetime import datetime

from lib.utils import bot
from sis.config import configFile, get_now_data
from sis.lang import langFile


def update_time_run(start_time):
    current_time = datetime.now()
    elapsed_time = current_time - start_time

    hours, remainder = divmod(elapsed_time.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    elapsed_time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    run(bot.editMessageText(chat_id=configFile['telegramChatId'], message_id=int(get_now_data('telegramMsgId')),
                            text="✅ " + elapsed_time_str))


async def stop_time_run():
    await bot.editMessageText(chat_id=configFile['telegramChatId'], message_id=int(get_now_data('telegramMsgId')),
                              text="🛑 " + langFile['stopedBot'])

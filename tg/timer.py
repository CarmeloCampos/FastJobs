from asyncio import run
from datetime import datetime

from lib.utils import get_bot
from sis.config import configFile, get_now_data
from sis.lang import langFile
from sis.temp import get_finder


async def edit_sync_msg(text):
    bot = get_bot()
    await bot.editMessageText(chat_id=configFile['telegramChatId'], message_id=int(get_now_data('telegramMsgId')),
                              text=text)
    await bot.close()


def edit_msg(text):
    run(edit_sync_msg(text))


def update_time_run(start_time):
    current_time = datetime.now()
    elapsed_time = current_time - start_time

    hours, remainder = divmod(elapsed_time.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    elapsed_time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    edit_msg("🛑 " + langFile['stopedBot'] if not get_finder() else "✅" + " " + elapsed_time_str)

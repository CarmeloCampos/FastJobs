from telegram import Update
from telegram.ext import ContextTypes

from lib.utils import bot
from sis.bot import flex
from sis.config import configFile
from sis.config import get_flex_data
from sis.engine import get_fresh_finder, reload_finder
from sis.lang import langFile
from sis.temp import get_finder, update_finding
from tg.timer import stop_time_run


async def first_run():
    run_msg = await bot.sendMessage(chat_id=configFile['telegramChatId'], text='00:00:00')
    await bot.pinChatMessage(chat_id=run_msg.chat.id, message_id=run_msg.message_id)
    flex.updateSelf('telegramMsgId', run_msg.message_id, skip_self=True)


async def search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    ready_login = get_flex_data('ready_login')
    if ready_login:
        if get_finder():
            await update.message.reply_text(langFile['searchInProgress'])
            return
        await update.message.reply_text(langFile['searching'])
        await first_run()
        get_fresh_finder().start()
        update_finding(True)
    else:
        await update.message.reply_text(langFile['needLogin'])


async def stop_search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if get_finder():
        update_finding(False)
        await update.message.reply_text(langFile['searchStopped'])
        await stop_time_run()
        reload_finder()
    else:
        await update.message.reply_text(langFile['noSearchInProgress'])

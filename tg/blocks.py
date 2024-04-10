from telegram import Update
from telegram.ext import ContextTypes

from sis.config import get_flex_data
from sis.engine import get_fresh_finder, reload_finder
from sis.lang import langFile
from sis.temp import get_finder, update_finding


async def search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    ready_login = get_flex_data('ready_login')
    if ready_login:
        if get_finder():
            await update.message.reply_text(langFile['searchInProgress'])
            return
        await update.message.reply_text(langFile['searching'])
        get_fresh_finder().start()
        update_finding(True)
    else:
        await update.message.reply_text(langFile['needLogin'])


async def stop_search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if get_finder():
        update_finding(False)
        await update.message.reply_text(langFile['searchStopped'])
        reload_finder()
    else:
        await update.message.reply_text(langFile['noSearchInProgress'])

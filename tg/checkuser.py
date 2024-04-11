from telegram import Update
from telegram.ext import ContextTypes

from sis.lang import langFile


async def restricted(update: Update, _conext: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(langFile['noAllowUser'])
    print(f"Unauthorized access denied for {update.message.from_user.id}.")
    return

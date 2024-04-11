from re import escape

from telegram import Update
from telegram.ext import Application, ContextTypes
from telegram.ext import ConversationHandler, filters

from sis.config import configFile
from sis.lang import langFile
from tg.menu import main_menu


async def set_commands(app: Application) -> None:
    await app.bot.set_my_commands([
        ('start', langFile['start']),
    ])


button_cancel = filters.Regex('^' + escape(langFile["backMenu"]) + '$')


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(langFile['processCanceled'], reply_markup=main_menu)
    return ConversationHandler.END


application = Application.builder().token(configFile["telegramToken"]).post_init(set_commands).build()

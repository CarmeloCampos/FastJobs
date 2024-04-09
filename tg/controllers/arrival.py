from telegram.ext import ConversationHandler

from sis.bot import flex
from sis.lang import langFile
from tg.menu import config_menu, arrival_menu


async def start_arrival(update, context):
    await update.message.reply_text(langFile['arrivalConfig'], reply_markup=arrival_menu)
    return 'WAITING_ARRIVAL_INFO'


async def update_arrival(update, context):
    arrival_minute = int(update.message.text.replace('m', ''))
    flex.updateSelf('arrivalBuffer', arrival_minute)
    await update.message.reply_text(langFile['arrivalUpdated'], reply_markup=config_menu)
    return ConversationHandler.END

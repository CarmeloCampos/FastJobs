from telegram.ext import ConversationHandler, MessageHandler, filters

from sis.bot import flex
from sis.lang import langFile
from tg.bot import cancel, button_cancel
from tg.menu import config_menu, arrival_menu


async def start_arrival(update, context):
    await update.message.reply_text(langFile['arrivalConfig'], reply_markup=arrival_menu)
    return 'WAITING_ARRIVAL_INFO'


async def update_arrival(update, context):
    arrival_minute = int(update.message.text.replace('m', ''))
    flex.updateSelf('arrivalBuffer', arrival_minute)
    await update.message.reply_text(langFile['arrivalUpdated'], reply_markup=config_menu)
    return ConversationHandler.END


conv_arrival = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('^' + langFile["arrivalBuffer"] + '$'), start_arrival)],
    states={
        'WAITING_ARRIVAL_INFO': [
            MessageHandler(filters.TEXT & filters.Regex(r'\b\d+m\b'), update_arrival),
            MessageHandler(filters.TEXT & ~button_cancel, start_arrival)
        ],
    },
    fallbacks=[MessageHandler(button_cancel, cancel)],
)

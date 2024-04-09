import re

from telegram.ext import ConversationHandler, MessageHandler, filters

from sis.lang import langFile
from tg.bot import cancel
from tg.controllers.arrival import start_arrival, update_arrival
from tg.controllers.block import start_block, update_block
from tg.controllers.hourly import start_hourly_pay, update_hourly_pay
from tg.menu import config_menu


async def start_configuration(update, context):
    await update.message.reply_text(langFile['initMenuOptions'], reply_markup=config_menu)
    return 'WAITING_FOR_ANYTHING'


async def any_message(update, context):
    await update.message.reply_text(langFile['initMenuOptions'], reply_markup=config_menu)
    return 'WAITING_FOR_ANYTHING'


button_cancel = filters.Regex('^' + re.escape(langFile["backMenu"]) + '$')

conv_hourly_pay = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('^' + langFile["hourlyPay"] + '$'), start_hourly_pay)],
    states={
        'WAITING_HOURLY_PAY': [MessageHandler(filters.TEXT, update_hourly_pay)],
    },
    fallbacks=[MessageHandler(button_cancel, cancel)],
)

conv_min_bloque = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('^' + langFile["blockPay"] + '$'), start_block)],
    states={
        'WAITING_BLOCK_PAY': [MessageHandler(filters.TEXT, update_block)],
    },
    fallbacks=[MessageHandler(button_cancel, cancel)],
)

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

conv_config = ConversationHandler(
    entry_points=[
        MessageHandler(filters.Regex('^' + re.escape(langFile["CONFIGURATIONS"]) + '$'), start_configuration)
    ],
    states={
        'WAITING_FOR_ANYTHING': [conv_hourly_pay, conv_min_bloque, conv_arrival,
                                 MessageHandler(filters.TEXT & ~button_cancel, any_message)],
    },
    fallbacks=[MessageHandler(button_cancel, cancel)],
)

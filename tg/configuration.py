import re

from telegram.ext import ConversationHandler, MessageHandler, filters

from sis.config import configFile, allow_admins
from sis.lang import langFile
from tg.bot import cancel, button_cancel
from tg.controllers.arrival import conv_arrival
from tg.controllers.block import conv_min_bloque
from tg.controllers.daysjobs import conv_days_jobs
from tg.controllers.hourly import conv_hourly_pay
from tg.controllers.hoursjobs import conv_hourly_jobs
from tg.menu import config_menu


async def start_configuration(update, context):
    await update.message.reply_text(langFile['initMenuOptions'], reply_markup=config_menu)
    return 'WAITING_FOR_ANYTHING'


async def any_message(update, context):
    await update.message.reply_text(langFile['initMenuOptions'], reply_markup=config_menu)
    return 'WAITING_FOR_ANYTHING'


conv_config = ConversationHandler(
    entry_points=[
        MessageHandler(filters.Regex('^' + re.escape(langFile["CONFIGURATIONS"]) + '$'), start_configuration)
    ],
    states={
        'WAITING_FOR_ANYTHING': [conv_hourly_pay, conv_min_bloque, conv_arrival, conv_days_jobs, conv_hourly_jobs,
                                 MessageHandler(filters.TEXT & ~button_cancel, any_message)],
    },
    fallbacks=[MessageHandler(button_cancel, cancel)],
)

allow_chats_id = filters.Chat(chat_id=configFile['telegramChatId'])
allow_chats_id.add_chat_ids(allow_admins)

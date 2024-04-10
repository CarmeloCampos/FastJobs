from telegram.ext import ConversationHandler, MessageHandler, filters

from sis.config import configFile
from sis.lang import langFile
from tg.bot import cancel, button_cancel
from tg.menu import time_menu


async def show_time_menu(update, context):
    await update.message.reply_text(langFile['selectMenuOptions'], reply_markup=time_menu)
    return 'SELECT_HOURS_JOBS'


async def show_actual_times(update, context):
    try:
        if update.message.text == langFile['currentStartTime']:
            await update.message.reply_text(configFile['desiredStartTime'], reply_markup=time_menu)
        else:
            await update.message.reply_text(configFile['desiredEndTime'], reply_markup=time_menu)
    finally:
        return 'SELECT_HOURS_JOBS'


async def update_actual_times(update, context):
    pass


conv_hourly_jobs = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('^' + langFile["selectHours"] + '$'), show_time_menu)],
    states={
        'SELECT_HOURS_JOBS': [
            MessageHandler(filters.Regex('^' + langFile["currentStartTime"] + '$'), show_actual_times),
            MessageHandler(filters.Regex('^' + langFile["currentEndTime"] + '$'), show_actual_times)
        ],
    },
    fallbacks=[MessageHandler(button_cancel, cancel)],
)

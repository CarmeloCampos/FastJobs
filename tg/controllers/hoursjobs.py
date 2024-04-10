from telegram.ext import ConversationHandler, MessageHandler, filters

from sis.bot import flex
from sis.config import get_now_data
from sis.lang import langFile
from tg.bot import cancel, button_cancel
from tg.menu import time_menu, hours_menu


async def show_time_menu(update, context):
    await update.message.reply_text(langFile['selectMenuOptions'], reply_markup=time_menu)
    return 'SELECT_HOURS_JOBS'


async def show_actual_times(update, context):
    try:
        if update.message.text == langFile['currentStartTime']:
            await update.message.reply_text(get_now_data('desiredStartTime'), reply_markup=time_menu)
        else:
            await update.message.reply_text(get_now_data('desiredEndTime'), reply_markup=time_menu)
    finally:
        return 'SELECT_HOURS_JOBS'


async def update_actual_times(update, type_time):
    flex.updateSelf(type_time, update.message.text)
    await update.message.reply_text(langFile['hourlyUpdated'], reply_markup=time_menu)
    return ConversationHandler.END


async def init_desired_start_time(update, waiting_type):
    await update.message.reply_text(langFile['initDesiredTime'], reply_markup=hours_menu)
    return waiting_type


regex_time = filters.Regex(r'([01]?[0-9]|2[0-3]):([0-5][0-9])')

conv_desired_start_time = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('^' + langFile["desiredStartTime"] + '$'),
                                 lambda u, c: init_desired_start_time(u, 'WAITING_DESIRED_START_TIME'))],
    states={
        'WAITING_DESIRED_START_TIME': [
            MessageHandler(regex_time, lambda u, c: update_actual_times(u, 'desiredStartTime'))],
    },
    fallbacks=[MessageHandler(button_cancel, cancel)],
)

conv_desired_end_time = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('^' + langFile["desiredEndTime"] + '$'),
                                 lambda u, c: init_desired_start_time(u, 'WAITING_DESIRED_END_TIME'))],
    states={
        'WAITING_DESIRED_END_TIME': [
            MessageHandler(regex_time, lambda u, c: update_actual_times(u, 'desiredEndTime'))],
    },
    fallbacks=[MessageHandler(button_cancel, cancel)],
)

conv_hourly_jobs = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('^' + langFile["selectHours"] + '$'), show_time_menu)],
    states={
        'SELECT_HOURS_JOBS': [
            MessageHandler(filters.Regex('^' + langFile["currentStartTime"] + '$'), show_actual_times),
            MessageHandler(filters.Regex('^' + langFile["currentEndTime"] + '$'), show_actual_times),
            conv_desired_start_time,
            conv_desired_end_time
        ],
    },
    fallbacks=[MessageHandler(button_cancel, cancel)],
)

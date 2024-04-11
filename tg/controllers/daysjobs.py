from telegram.ext import ConversationHandler, MessageHandler, filters

from sis.bot import flex
from sis.config import get_now_data
from sis.lang import langFile
from tg.bot import cancel, button_cancel
from tg.menu import days_menu, select_days_menu, config_menu


async def show_days_menu(update, context):
    if update.message.text == langFile["selectDays"]:
        await update.message.reply_text(langFile['selectMenuOptions'], reply_markup=days_menu)
    elif update.message.text == langFile["add"]:
        await update.message.reply_text(langFile['selectMenuOptions'], reply_markup=select_days_menu)
    return 'SELECT_DAYS_JOBS'


async def show_actual_days(update, context):
    try:
        if len(get_now_data('desiredWeekdays')) > 0:
            await update.message.reply_text(", ".join(get_now_data('desiredWeekdays')), reply_markup=days_menu)
        elif len(get_now_data('desiredWeekdays')) == 0:
            await update.message.reply_text(langFile['noConfigDays'], reply_markup=days_menu)
    finally:
        return 'SELECT_DAYS_JOBS'

async def clear_actual_days(update, context):
    flex.updateSelf('desiredWeekdays', [])
    await update.message.reply_text(langFile['clearDesiredWeekdays'], reply_markup=days_menu)


async def update_days_list(update, context):
    weekDays = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
    if update.message.text == langFile['backConfig']:
        await update.message.reply_text(langFile['selectMenuOptions'], reply_markup=config_menu)
        return ConversationHandler.END
    elif update.message.text not in get_now_data('desiredWeekdays') and update.message.text != langFile['backSelectDays'] and update.message.text in weekDays:
        list = get_now_data('desiredWeekdays')
        list.append(update.message.text)
        flex.updateSelf('desiredWeekdays', list)
        await update.message.reply_text(langFile['addNewDay'].format(update.message.text))
        return 'SELECT_DAYS_JOBS'
    elif update.message.text == langFile['backSelectDays']:
        await update.message.reply_text(langFile['selectMenuOptions'], reply_markup=days_menu)
        return 'SELECT_DAYS_JOBS'
    else:
        await update.message.reply_text(langFile['alreadyInList'], reply_markup=select_days_menu)
        return 'SELECT_DAYS_JOBS'


conv_days_jobs = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('^' + langFile["selectDays"] + '$'), show_days_menu)],
    states={
        'SELECT_DAYS_JOBS': [
            MessageHandler(filters.Regex('^' + langFile["actualConfigDays"] + '$'), show_actual_days),
            MessageHandler(filters.Regex('^' + langFile["add"] + '$'), show_days_menu),
            MessageHandler(filters.Regex('^' + langFile["remove"] + '$'), clear_actual_days),
            MessageHandler(filters.TEXT, update_days_list)
        ],
    },
    fallbacks=[MessageHandler(button_cancel, cancel)],
)

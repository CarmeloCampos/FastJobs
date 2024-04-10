from sis.config import configFile
from sis.lang import langFile
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

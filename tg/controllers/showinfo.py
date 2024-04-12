from telegram.ext import ConversationHandler, MessageHandler, filters

from tg.bot import cancel, button_cancel
from sis.lang import langFile
from sis.config import get_now_data
from tg.menu import config_menu


async def send_actual_config_info(update, context):
    actualInfo = f""" {langFile['currentData']}\n
{langFile['hourlyPay']}: {get_now_data('minPayRatePerHour')} $\n
{langFile['blockPay']}: {get_now_data('minBlockRate')} $\n
{langFile['arrivalBuffer']}: {get_now_data('arrivalBuffer')} Minutos\n
{langFile['actualConfigDays']}: {(", ".join(get_now_data('desiredWeekdays')))}\n
{langFile['desiredStartTime']}: {get_now_data('desiredStartTime')}\n
{langFile['desiredEndTime']}: {get_now_data('desiredEndTime')}\n
"""

    await update.message.reply_text(actualInfo, reply_markup=config_menu)
    return 'WAITING_FOR_ANYTHING'

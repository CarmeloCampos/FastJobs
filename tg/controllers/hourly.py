from telegram import ReplyKeyboardRemove
from telegram.ext import ConversationHandler, MessageHandler, filters

from sis.bot import flex
from sis.lang import langFile
from tg.bot import cancel, button_cancel
from tg.menu import config_menu


async def start_hourly_pay(update, context):
    await update.message.reply_text(langFile['whatIsYourMinHourPay'], reply_markup=ReplyKeyboardRemove())
    return 'WAITING_HOURLY_PAY'


async def update_hourly_pay(update, context):
    if not update.message.text.isdigit():
        await update.message.reply_text(langFile['payInvalid'], reply_markup=ReplyKeyboardRemove())
        return 'WAITING_HOURLY_PAY'
    flex.updateSelf('minPayRatePerHour', int(update.message.text))
    await update.message.reply_text(langFile['hourlyPayUpdated'], reply_markup=config_menu)
    return ConversationHandler.END


conv_hourly_pay = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('^' + langFile["hourlyPay"] + '$'), start_hourly_pay)],
    states={
        'WAITING_HOURLY_PAY': [MessageHandler(filters.TEXT, update_hourly_pay)],
    },
    fallbacks=[MessageHandler(button_cancel, cancel)],
)

from telegram import ReplyKeyboardRemove
from telegram.ext import ConversationHandler, MessageHandler, filters

from sis.bot import flex
from sis.lang import langFile
from tg.bot import cancel, button_cancel
from tg.menu import config_menu


async def start_block(update, context):
    await update.message.reply_text(langFile['whatIsYourMinBlockPay'], reply_markup=ReplyKeyboardRemove())
    return 'WAITING_BLOCK_PAY'


async def update_block(update, context):
    if not update.message.text.isdigit():
        await update.message.reply_text(langFile['payInvalid'], reply_markup=ReplyKeyboardRemove())
        return 'WAITING_BLOCK_PAY'
    flex.updateSelf('minBlockRate', int(update.message.text))
    await update.message.reply_text(langFile['blockPayUpdated'], reply_markup=config_menu)
    return ConversationHandler.END


conv_min_bloque = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('^' + langFile["blockPay"] + '$'), start_block)],
    states={
        'WAITING_BLOCK_PAY': [MessageHandler(filters.TEXT, update_block)],
    },
    fallbacks=[MessageHandler(button_cancel, cancel)],
)

from telegram import ReplyKeyboardRemove
from telegram.ext import ConversationHandler

from sis.bot import flex
from sis.lang import langFile
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

from telegram.ext import Application

from sis.config import configFile
from sis.lang import langFile
from tg.menu import main_menu, config_menu, time_menu


async def set_commands(app: Application) -> None:
    await app.bot.set_my_commands([
        ('start', langFile['start']),
    ])

async def handle_message(update, context):
    user_message = update.message.text

    try:
        if user_message == langFile['CONFIGURATIONS']:
            await update.message.reply_text(langFile['initMenuOptions'], reply_markup=config_menu)
        elif user_message == langFile['backMenu']:
            await update.message.reply_text(langFile['initMenuOptions'],reply_markup=main_menu)
        elif user_message == langFile['backConfig']:
            await update.message.reply_text(langFile['initMenuOptions'], reply_markup=config_menu)
        elif user_message == langFile['selectHours']:
            await update.message.reply_text(langFile['selectMenuOptions'], reply_markup=time_menu)
        elif user_message == langFile['currentStartTime']:
            await update.message.reply_text(f"{langFile['currentStartTimeConfig']} {configFile['desiredStartTime']}")
        elif user_message == langFile['currentEndTime']:
            await update.message.reply_text(f"{langFile['currentEndTimeConfig']} {configFile['desiredEndTime']}")
    finally:
        await context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)


application = Application.builder().token(configFile["telegramToken"]).post_init(set_commands).build()

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters

from sis.lang import langFile
from tg.blocks import search, stop_search
from tg.bot import application, handle_message
from tg.start_login import start, login

LOGIN = 0


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(langFile['processCanceled'])
    return ConversationHandler.END


def main() -> None:
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LOGIN: [MessageHandler(
                filters.Regex('^https://(www.)?amazon.[a-z]{2,}/.*[?&]openid.oa2.authorization_code=.*'), login
            )],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    application.add_handler(MessageHandler(filters.Regex('^' + langFile["SEARCHBLOCK"] + '$'), search))
    application.add_handler(MessageHandler(filters.Regex('^' + langFile["STOPSEARCH"] + '$'), stop_search))
    application.add_handler(MessageHandler(filters.Regex('^' + langFile["CONFIGURATIONS"] + '$'), handle_message))
    application.add_handler(MessageHandler(filters.Regex('^' + langFile["selectHours"] + '$'), handle_message))
    application.add_handler(MessageHandler(filters.Regex('^' + langFile["backMenu"] + '$'), handle_message))
    application.add_handler(MessageHandler(filters.Regex('^' + langFile["backConfig"] + '$'), handle_message))
    application.add_handler(MessageHandler(filters.Regex('^' + langFile["currentStartTime"] + '$'), handle_message))
    application.add_handler(MessageHandler(filters.Regex('^' + langFile["currentEndTime"] + '$'), handle_message))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

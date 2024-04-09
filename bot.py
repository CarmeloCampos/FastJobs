from telegram import Update
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, filters

from sis.lang import langFile
from tg.blocks import search, stop_search
from tg.bot import application, cancel
from tg.configuration import conv_config
from tg.start_login import start, login


def main() -> None:
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            'LOGIN': [MessageHandler(
                filters.Regex('^https://(www.)?amazon.[a-z]{2,}/.*[?&]openid.oa2.authorization_code=.*'), login
            )],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    application.add_handler(conv_config)
    application.add_handler(MessageHandler(filters.Regex('^' + langFile["SEARCHBLOCK"] + '$'), search))
    application.add_handler(MessageHandler(filters.Regex('^' + langFile["STOPSEARCH"] + '$'), stop_search))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

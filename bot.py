import json
from threading import Thread, Event

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters

from lib.FlexUnlimited import FlexUnlimited
from tg.menu import MenuMain

flex = FlexUnlimited()
waiting_login = False
code_verifier = ''
ReadyLogin = False
Finding = None
Finder = None
configFile = json.load(open('config.json'))

LOGIN, FIND = range(2)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send a message when the command /start is issued."""
    global waiting_login, code_verifier, ReadyLogin
    if flex.needLogin():
        await update.message.reply_text("Necesitas iniciar sesión")
        link, code_verifier = flex.generate_challenge_link()
        await update.message.reply_text(link)
        waiting_login = True
        return LOGIN
    else:
        await update.message.reply_text("Ya estás logueado", reply_markup=MenuMain())
        ReadyLogin = True


async def login(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global waiting_login, code_verifier, ReadyLogin
    if waiting_login:
        try:
            if flex.registerAccount(update.message.text, code_verifier):
                await update.message.reply_text("Has iniciado sesión", reply_markup=MenuMain())
                ReadyLogin = True
            else:
                await update.message.reply_text("No has podido iniciar sesión")
        except Exception as e:
            await update.message.reply_text("No has podido iniciar sesión")
    else:
        await update.message.reply_text("No necesitas iniciar sesión", reply_markup=MenuMain())


async def buscar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global ReadyLogin, Finder, Finding
    if ReadyLogin:
        if Finder is not None:
            await update.message.reply_text("Ya hay una búsqueda en curso")
            return
        Finding = Event()
        await update.message.reply_text("Buscando bloques...")
        Finder = Thread(target=flex.run, args=(Finding, update))
        Finder.start()
    else:
        await update.message.reply_text("Necesitas iniciar sesión con /start")


async def startTime(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ Envía un mensaje con la información de la hora de inicio de trabajo deseada"""
    await update.message.reply_text(f"La hora de inicio deseada es: {configFile["desiredStartTime"]}")


async def changeStartTime(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ Envía un mensaje con la información de la hora de inicio de trabajo deseada"""
    await update.message.reply_text(f"La hora de inicio deseada es: 12")


async def endTime(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ Envía un mensaje con la información de la hora de finalización de trabajo deseada"""
    await update.message.reply_text(f"La hora de finalización deseada es: {configFile["desiredEndTime"]}")


# Define tus comandos
commandos = [
    ('start', 'Iniciar el bot'),
]


async def postInit(application: Application) -> None:
    await application.bot.set_my_commands(commandos)


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global Finding, Finder
    if Finder is not None:
        Finding.set()
        Finder = None
        await update.message.reply_text("Búsqueda detenida")
    else:
        await update.message.reply_text("No hay búsqueda en curso")


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Operación cancelada")
    return ConversationHandler.END


def main() -> None:
    """Start the bot."""
    application = Application.builder().token(configFile["telegramToken"]).post_init(postInit).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LOGIN: [MessageHandler(
                filters.Regex('^https://(www.)?amazon.[a-z]{2,}/.*[?&]openid.oa2.authorization_code=.*'),
                login)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    application.add_handler(MessageHandler(filters.Regex('^BUSCAR$'), buscar))
    application.add_handler(MessageHandler(filters.Regex('^DETER BUSQUEDA$'), stop))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

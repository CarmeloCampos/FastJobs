from threading import Thread, Event
import json

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from lib.FlexUnlimited import FlexUnlimited

flex = FlexUnlimited()
waiting_login = False
code_verifier = ''
ReadyLogin = False
Finding = None
Finder = None
configFile = json.load(open('config.json'))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    global waiting_login, code_verifier, ReadyLogin
    if flex.needLogin():
        await update.message.reply_text("Necesitas iniciar sesión")
        link, code_verifier = flex.generate_challenge_link()
        await update.message.reply_text(link)
        waiting_login = True
    else:
        await update.message.reply_text("Ya estás logueado")
        ReadyLogin = True


async def login(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /login is issued."""
    global waiting_login, code_verifier, ReadyLogin
    if waiting_login:
        try:
            flex.registerAccount(context.args[0], code_verifier)
            await update.message.reply_text("Has iniciado sesión")
            ReadyLogin = True
        except Exception as e:
            await update.message.reply_text("No has podido iniciar sesión")
    else:
        await update.message.reply_text("No necesitas iniciar sesión")


async def buscar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /buscar is issued."""
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
    ('login', 'Iniciar sesión'),
    ('buscar', 'Buscar algo'),
    ('ver_hora_inicio', 'Mostrar hora preferida para inicio del bloque.'),
    ('cambiar_hora_inicio', 'Cambia hora preferida para inicio del bloque.'),
    ('ver_hora_fin', 'Mostrar hora preferida para finalización del bloque.'),
    ('cambiar_hora_fin', 'Cambia hora preferida para finalización del bloque.'),
    ('stop', 'Detener búsqueda')
]

async def postInit(application: Application) -> None:
    await application.bot.set_my_commands(commandos)


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /stop is issued."""
    global Finding, Finder
    if Finder is not None:
        Finding.set()
        Finder = None
        await update.message.reply_text("Búsqueda detenida")
    else:
        await update.message.reply_text("No hay búsqueda en curso")


def main() -> None:
    """Start the bot."""
    application = Application.builder().token(configFile["telegramToken"]).post_init(postInit).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("login", login))
    application.add_handler(CommandHandler("buscar", buscar))
    application.add_handler(CommandHandler("ver_hora_inicio", startTime))
    application.add_handler(CommandHandler("cambiar_hora_inicio", changeStartTime))
    application.add_handler(CommandHandler("ver_hora_fin", endTime))
    application.add_handler(CommandHandler("stop", stop))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

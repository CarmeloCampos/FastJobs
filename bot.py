from threading import Thread, Event

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from lib.FlexUnlimited import FlexUnlimited

flex = FlexUnlimited()
waiting_login = False
code_verifier = ''
ReadyLogin = False
Finding = None
Finder = None


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
    application = Application.builder().token("648441948:AAH8vrwq4lrCfc4Sz8z4pVE_ZvCbRpq-V6A").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("login", login))
    application.add_handler(CommandHandler("buscar", buscar))
    application.add_handler(CommandHandler("stop", stop))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

from telegram import ReplyKeyboardMarkup


def MenuMain():
    reply_keyboard = [["BUSCAR", "DETER BUSQUEDA", "CONFIGURACIONES"]]
    return ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

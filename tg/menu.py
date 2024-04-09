from telegram import ReplyKeyboardMarkup

from sis.lang import langFile

main_menu = ReplyKeyboardMarkup([
    [langFile['SEARCHBLOCK'], langFile['STOPSEARCH']],
    [langFile['CONFIGURATIONS']]
], resize_keyboard=True)

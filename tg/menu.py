from telegram import ReplyKeyboardMarkup

from sis.lang import langFile

main_menu = ReplyKeyboardMarkup([
    [langFile['SEARCHBLOCK'], langFile['STOPSEARCH']],
    [langFile['CONFIGURATIONS']]
], resize_keyboard=True)


config_menu = ReplyKeyboardMarkup([
    [langFile['hourlyPay'], langFile['selectHours']],
    [langFile['selectDays'], langFile['language']],
    [langFile['backMenu']]
], resize_keyboard=True)


time_menu = ReplyKeyboardMarkup([
    [langFile['currentStartTime'], langFile['currentEndTime']],
    [langFile['desiredStartTime'], langFile['desiredEndTime']],
    [langFile['backConfig']]
], resize_keyboard=True)

from telegram import ReplyKeyboardMarkup

from sis.lang import langFile

main_menu = ReplyKeyboardMarkup([
    [langFile['SEARCHBLOCK'], langFile['STOPSEARCH']],
    [langFile['CONFIGURATIONS']]
], resize_keyboard=True)

config_menu = ReplyKeyboardMarkup([
    [langFile['hourlyPay'], langFile['blockPay'], langFile['arrivalBuffer']],
    [langFile['selectDays'], langFile['selectHours']],
    [langFile['backMenu']]
], resize_keyboard=True)

time_menu = ReplyKeyboardMarkup([
    [langFile['currentStartTime'], langFile['currentEndTime']],
    [langFile['desiredStartTime'], langFile['desiredEndTime']],
    [langFile['backConfig']]
], resize_keyboard=True)

arrival_menu = ReplyKeyboardMarkup([["15m", "30m", "45m"]], resize_keyboard=True)

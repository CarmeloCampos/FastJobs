from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler, MessageHandler, filters

from sis.areas import fetch_and_update_wire_houses
from sis.bot import flex
from sis.config import get_now_data
from sis.lang import langFile
from tg.bot import cancel, button_cancel
from tg.menu import config_menu

all_wire_house = {}


async def what_wire_house(update, context):
    global all_wire_house
    await update.message.reply_text(langFile['loadingWireHouse'], reply_markup=ReplyKeyboardRemove())
    all_wire_house = await fetch_and_update_wire_houses()
    servicesAll = [[langFile['backConfig']]]
    servicesAll.extend([[name] for name in all_wire_house.keys()])

    await update.message.reply_text(langFile['whatWireHouse'], reply_markup=ReplyKeyboardMarkup(servicesAll))
    return 'SELECT_WIRE_HOUSE'


async def update_wire_house(update, context):
    global all_wire_house
    wire_house = update.message.text
    if wire_house == langFile['backConfig']:
        await update.message.reply_text(langFile['selectMenuOptions'], reply_markup=config_menu)
        return ConversationHandler.END
    elif wire_house not in all_wire_house:
        await update.message.reply_text(langFile['wireHouseInvalid'])
        return 'SELECT_WIRE_HOUSE'
    service_area_id = all_wire_house[wire_house]
    list_now = get_now_data('desiredWarehouses')
    if service_area_id in list_now:
        await update.message.reply_text(langFile['alreadyInListWireHouse'])
        return 'SELECT_WIRE_HOUSE'
    list_now.append(service_area_id)
    flex.updateSelf('desiredWarehouses', list_now)
    await update.message.reply_text(langFile['wireHouseUpdated'], reply_markup=config_menu)

    return ConversationHandler.END


conv_set_wirehouse = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('^' + langFile["setWireHouse"] + '$'), what_wire_house)],
    states={
        'SELECT_WIRE_HOUSE': [
            MessageHandler(filters.TEXT, update_wire_house)
        ],
    },
    fallbacks=[MessageHandler(button_cancel, cancel)],
)

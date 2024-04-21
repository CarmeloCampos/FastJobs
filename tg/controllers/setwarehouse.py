from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler, MessageHandler, filters

from sis.areas import fetch_and_update_ware_houses
from sis.bot import flex
from sis.config import get_now_data
from sis.lang import langFile
from tg.bot import cancel, button_cancel
from tg.menu import config_menu

all_ware_house = {}


async def what_ware_house(update, context):
    global all_ware_house
    await update.message.reply_text(langFile['loadingWareHouse'], reply_markup=ReplyKeyboardRemove())
    all_ware_house = await fetch_and_update_ware_houses()
    servicesAll = [[langFile['backConfig']]]
    servicesAll.extend([[name] for name in all_ware_house.keys()])

    await update.message.reply_text(langFile['whatWareHouse'], reply_markup=ReplyKeyboardMarkup(servicesAll))
    return 'SELECT_WARE_HOUSE'


async def update_ware_house(update, context):
    global all_ware_house
    ware_house = update.message.text
    if ware_house == langFile['backConfig']:
        await update.message.reply_text(langFile['selectMenuOptions'], reply_markup=config_menu)
        return ConversationHandler.END
    elif ware_house not in all_ware_house:
        await update.message.reply_text(langFile['wareHouseInvalid'])
        return 'SELECT_WARE_HOUSE'
    service_area_id = all_ware_house[ware_house]
    list_now = get_now_data('desiredWarehouses')
    if service_area_id in list_now:
        await update.message.reply_text(langFile['alreadyInListWareHouse'])
        return 'SELECT_WARE_HOUSE'
    list_now.append(service_area_id)
    flex.updateSelf('desiredWarehouses', list_now)
    await update.message.reply_text(langFile['wareHouseUpdated'], reply_markup=config_menu)

    return ConversationHandler.END


conv_set_warehouse = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('^' + langFile["setWareHouse"] + '$'), what_ware_house)],
    states={
        'SELECT_WARE_HOUSE': [
            MessageHandler(filters.TEXT, update_ware_house)
        ],
    },
    fallbacks=[MessageHandler(button_cancel, cancel)],
)

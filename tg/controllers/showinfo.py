from sis.areas import fetch_and_update_wire_houses
from sis.bot import flex
from sis.config import get_now_data
from sis.lang import langFile
from tg.menu import config_menu


async def send_actual_config_info(update, context):
    all_wire_house = await fetch_and_update_wire_houses()

    service_areas = flex.getAllServiceAreas()
    wire_house_dict = {wh['serviceAreaId']: wh['serviceAreaName'] for wh in service_areas}

    min_pay_rate_per_hour = get_now_data('minPayRatePerHour')
    min_block_rate = get_now_data('minBlockRate')
    arrival_buffer = get_now_data('arrivalBuffer')
    desired_weekdays = get_now_data('desiredWeekdays')
    desired_start_time = get_now_data('desiredStartTime')
    desired_end_time = get_now_data('desiredEndTime')
    desired_warehouses = get_now_data('desiredWarehouses')

    warehouse_names = [wire_house_dict.get(wh_id, wh_id) for wh_id in desired_warehouses]

    actualInfo = f""" {langFile['currentData']}\n
{langFile['hourlyPay']}: {min_pay_rate_per_hour} $\n
{langFile['blockPay']}: {min_block_rate} $\n
{langFile['arrivalBuffer']}: {arrival_buffer} {langFile['minutes']}\n
{langFile['actualConfigDays']}: {", ".join(desired_weekdays) if desired_weekdays else langFile['allDays']}\n
{langFile['desiredStartTime']}: {desired_start_time}\n
{langFile['desiredEndTime']}: {desired_end_time}\n\n
{langFile['actualWireHouse']}: {"\n" + ("\n".join(warehouse_names) if desired_warehouses else langFile['allWireHouse'])}
"""

    await update.message.reply_text(actualInfo, reply_markup=config_menu)
    return 'WAITING_FOR_ANYTHING'

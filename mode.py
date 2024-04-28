from datetime import datetime

import json


def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def convert_epoch_to_datetime(epoch):
    return datetime.fromtimestamp(epoch)


def is_within_desired_time(start_time, end_time, config):
    desired_start_time = datetime.strptime(config["desiredStartTime"], "%H:%M").time()
    desired_end_time = datetime.strptime(config["desiredEndTime"], "%H:%M").time()
    return start_time.time() >= desired_start_time and end_time.time() <= desired_end_time


def is_valid_weekday(start_time, config):
    if not config["desiredWeekdays"]:
        return True
    weekday = start_time.strftime("%A").lower()
    return weekday in config["desiredWeekdays"]


config = load_json("json/config.json")
current_offers = load_json("json/currentOffers.json")

valid_offers = []

for offer in current_offers:
    if offer["serviceAreaId"] in config["desiredWarehouses"]:
        start_time = convert_epoch_to_datetime(offer["startTime"])
        end_time = convert_epoch_to_datetime(offer["endTime"])

        if is_valid_weekday(start_time, config) and is_within_desired_time(start_time, end_time, config):
            duration_hours = (end_time - start_time).total_seconds() / 3600
            min_pay_rate_per_hour = config['minPayRatePerHour']
            print("Valid week")

            if (offer['rateInfo']['priceAmount'] / duration_hours) >= min_pay_rate_per_hour:
                print("Oferta valida")
                valid_offers.append(offer)

print(f'aaaa: {len(valid_offers)}')
for valid_offer in valid_offers:
    print(valid_offer)

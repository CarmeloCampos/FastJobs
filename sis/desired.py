from datetime import datetime


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


def is_valid_offer(offer, config):
    start_time = convert_epoch_to_datetime(offer.get("startTime"))
    end_time = convert_epoch_to_datetime(offer.get("endTime"))
    return is_within_desired_time(start_time, end_time, config) and is_valid_weekday(start_time, config)

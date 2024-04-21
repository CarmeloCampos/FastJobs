from datetime import datetime
from sis.lang import langFile
from sis.bot import flex


class Offer:

    def __init__(self, offerResponseObject: object) -> None:
        self.id = offerResponseObject.get("offerId")
        self.expirationDate = datetime.fromtimestamp(offerResponseObject.get("expirationDate"))
        self.startTime = datetime.fromtimestamp(offerResponseObject.get("startTime"))
        self.location = offerResponseObject.get('serviceAreaId')
        self.blockRate = float(offerResponseObject.get('rateInfo').get('priceAmount'))
        self.endTime = datetime.fromtimestamp(offerResponseObject.get('endTime'))
        self.hidden = offerResponseObject.get("hidden")
        self.ratePerHour = round(self.blockRate / ((self.endTime - self.startTime).seconds / 3600), 2)
        self.weekday = self.expirationDate.weekday()

    def get_service_area_name(self, service_area_id):
        service_areas = flex.getAllServiceAreas()
        for area in service_areas:
            if area['serviceAreaId'] == service_area_id:
                return area['serviceAreaName']
        return None

    def toString(self) -> str:
        blockDuration = (self.endTime - self.startTime).seconds / 3600
        areaName = self.get_service_area_name(self.location)

        body = langFile['Location'] + areaName + '\n'
        body += langFile['Date'] + str(self.startTime.month) + '/' + str(self.startTime.day) + '\n'
        body += langFile['Pay'] + str(self.blockRate) + '\n'
        body += langFile['Pay rate per hour'] + str(self.ratePerHour) + '\n'
        body += (langFile['Block Duration'] + str(blockDuration) +
                 f'{langFile['Hour'] if blockDuration == 1 else langFile['Hours']}\n')

        if not self.startTime.minute:
            body += langFile['Start Time'] + str(self.startTime.hour) + '00\n'
        elif self.startTime.minute < 10:
            body += langFile['Start Time'] + str(self.startTime.hour) + '0' + str(self.startTime.minute) + '\n'
        else:
            body += langFile['Start Time'] + str(self.startTime.hour) + str(self.startTime.minute) + '\n'

        if not self.endTime.minute:
            body += langFile['End Time'] + str(self.endTime.hour) + '00\n'
        elif self.endTime.minute < 10:
            body += langFile['End Time'] + str(self.endTime.hour) + '0' + str(self.endTime.minute) + '\n'
        else:
            body += langFile['End Time'] + str(self.endTime.hour) + str(self.endTime.minute) + '\n'

        return body

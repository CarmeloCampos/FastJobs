from datetime import datetime
from urllib.parse import quote

from sis.config import get_now_data
from sis.lang import langFile
from sis.twilio import twilioClient


class Offer:

    def __init__(self, offerResponseObject: object, service_areas) -> None:
        self.id = offerResponseObject.get("offerId")
        self.expirationDate = datetime.fromtimestamp(offerResponseObject.get("expirationDate"))
        self.startTime = datetime.fromtimestamp(offerResponseObject.get("startTime"))
        self.location = offerResponseObject.get('serviceAreaId')
        self.blockRate = float(offerResponseObject.get('rateInfo').get('priceAmount'))
        self.endTime = datetime.fromtimestamp(offerResponseObject.get('endTime'))
        self.hidden = offerResponseObject.get("hidden")
        self.ratePerHour = round(self.blockRate / ((self.endTime - self.startTime).seconds / 3600), 2)
        self.weekday = self.expirationDate.weekday()
        self.service_areas = service_areas

    def generate_google_calendar_url(self) -> str:
        name = self.get_service_area_name()
        title = quote(f"Job: {name} - FastJobs")
        start = self.startTime.strftime('%Y%m%dT%H%M%S')
        end = self.endTime.strftime('%Y%m%dT%H%M%S')
        details = quote(self.toString())
        location = quote(name)

        url = f"https://www.google.com/calendar/event?action=TEMPLATE&text={title}&dates={start}/{end}&details={details}&location={location}&trp=false"

        return url

    def get_service_area_name(self):
        for area in self.service_areas:
            if area['serviceAreaId'] == self.location:
                return area['serviceAreaName']
        return None

    def toString(self) -> str:
        blockDuration = (self.endTime - self.startTime).seconds / 3600
        areaName = self.get_service_area_name()

        body = langFile['bloqueAceptado'] + '\n'
        body += langFile['Location'] + areaName + '\n'
        body += langFile['Date'] + self.startTime.strftime('%d/%m/%y') + '\n'
        body += langFile['Pay'] + str(self.blockRate) + '\n'
        body += langFile['Pay rate per hour'] + str(self.ratePerHour) + '\n'
        body += (langFile['Block Duration'] + str(blockDuration) +
                 f'{langFile['Hour'] if blockDuration == 1 else langFile['Hours']}\n')

        body += langFile['Start Time'] + self.startTime.strftime('%H:%M') + '\n'
        body += langFile['End Time'] + self.endTime.strftime('%H:%M') + '\n'

        return body

    def twilio_send(self):
        to_number = get_now_data('phoneNum')
        from_number = "+17864604281"
        twilioClient.messages.create(
            to=to_number,
            from_=from_number,
            body=self.toString())
        twilioClient.calls.create(
            to=to_number,
            from_=from_number,
            twiml='<Response><Say>' + langFile["callAcceptBloque"].format(self.startTime.strftime('%d/%m'),
                                                                          self.startTime.strftime('%H:%M'))
                  + '</Say></Response>'
        )

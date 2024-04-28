from datetime import datetime
from urllib.parse import quote

from sis.config import get_now_data
from sis.lang import langFile
from sis.twilio import twilioClient


class Offer:
    def __init__(self, offerResponseObject: object, service_areas) -> None:
        self.offer_data = offerResponseObject
        self.service_areas = service_areas

    def block_rate(self):
        return float(self.offer_data.get('rateInfo').get('priceAmount'))

    def start_time(self):
        return datetime.fromtimestamp(self.offer_data.get("startTime"))

    def end_time(self):
        return datetime.fromtimestamp(self.offer_data.get("endTime"))

    def expiration_date(self):
        return datetime.fromtimestamp(self.offer_data.get("expirationDate"))

    def rate_per_hour(self):
        time_delta = self.end_time() - self.start_time()
        return round(self.block_rate() / (time_delta.seconds / 3600), 2)

    def get_service_area_name(self):
        location = self.offer_data.get('serviceAreaId')
        for area in self.service_areas:
            if area['serviceAreaId'] == location:
                return area['serviceAreaName']
        return None

    def generate_google_calendar_url(self):
        title = quote(f"Job: {self.get_service_area_name()} - FastJobs")
        start = self.start_time().strftime('%Y%m%dT%H%M%S')
        end = self.end_time().strftime('%Y%m%dT%H%M%S')
        details = quote(self.toString())
        location = quote(self.get_service_area_name())
        return f"https://www.google.com/calendar/event?action=TEMPLATE&text={title}&dates={start}/{end}&details={details}&location={location}&trp=false"

    def toString(self):
        duration = (self.end_time() - self.start_time()).seconds / 3600
        area_name = self.get_service_area_name()
        duration_string = f"{duration} {'Hour' if duration == 1 else 'Hours'}"

        details = [
            langFile['bloqueAceptado'],
            f"{langFile['Location']}: {area_name}",
            f"{langFile['Date']}: {self.start_time().strftime('%d/%m/%Y')}",
            f"{langFile['Start Time']}: {self.start_time().strftime('%H:%M')}",
            f"{langFile['End Time']}: {self.end_time().strftime('%H:%M')}",
            f"{langFile['Pay']}: {self.block_rate()} USD",
            f"{langFile['Pay rate per hour']}: {self.rate_per_hour()} USD/Hr",
            f"{langFile['Block Duration']}: {duration_string}"
        ]

        return '\n'.join(details)

    def twilio_send(self):
        try:
            to_number = get_now_data('phoneNum')
            from_number = "+17864604281"

            call_time = self.start_time().strftime('%d/%m %H:%M')
            message = langFile["callAcceptBloque"].format(call_time)
            twiml_response = f"<Response><Say>{message}</Say></Response>"

            call = twilioClient.calls.create(
                to=to_number,
                from_=from_number,
                twiml=twiml_response
            )
            print(f"Call initiated, Call SID: {call.sid}")

        except Exception as e:
            print(f"Error initiating call with Twilio: {e}")

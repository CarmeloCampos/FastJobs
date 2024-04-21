from sis.bot import flex


async def fetch_and_update_ware_houses():
    service_areas = flex.getAllServiceAreas()
    return {serviceArea['serviceAreaName']: serviceArea['serviceAreaId'] for serviceArea in service_areas}

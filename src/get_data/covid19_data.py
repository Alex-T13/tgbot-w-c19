from typing import Optional
from fastapi import status

from config import settings
from custom_logging import logger
from get_data.data_types import Cv19Location, FuncParameters
from localization.translator import Translator
from utils import line_bit


async def covid19_data(args: FuncParameters) -> Optional[str]:
    if args.message.text == "/cv19belarus":
        url = "https://vaccovid-coronavirus-vaccine-and-treatment-tracker.p.rapidapi.com/api/npm-covid-data/" \
              "country-report-iso-based/Belarus/blr"
    else:
        url = f"https://vaccovid-coronavirus-vaccine-and-treatment-tracker.p.rapidapi.com/api/npm-covid-data/world"
    headers = {
        'x-rapidapi-key': f"{settings.x_rapidapi_key}",
        'x-rapidapi-host': "vaccovid-coronavirus-vaccine-and-treatment-tracker.p.rapidapi.com"
    }
    response = await args.session.get(url, headers=headers)

    if response.status != status.HTTP_200_OK:
        logger.warning("vaccovid-coronavirus api call failed: %s", response)
        body = await response.text()
        logger.debug(body)
        return None

    payload = await response.json()
    obj_format = Cv19Location(**payload[0])
    new_dict_resp = {
        'Total cases': line_bit(obj_format.TotalCases),
        'New cases': line_bit(obj_format.NewCases),
        'Total deaths': line_bit(obj_format.TotalDeaths),
        'New deaths': line_bit(obj_format.NewDeaths),
        'Total recovered': line_bit(obj_format.TotalRecovered),
        'New recovered': line_bit(obj_format.NewRecovered),
        'Active cases': line_bit(obj_format.ActiveCases),
        'Total tests': line_bit(obj_format.TotalTests),
    }

    return Translator.data_translation(loc=args.localization, data=new_dict_resp)

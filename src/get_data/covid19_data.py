from typing import Optional
from fastapi import status

from config import settings
from custom_logging import logger
from get_data.data_types import Cv19Location
from localization.translator import Translator
from utils import FuncParameters


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
    logger.debug(payload)

    obj_format = Cv19Location(**payload[0])

    new_dict_resp = {
        'Total cases': obj_format.TotalCases,
        'New cases': obj_format.NewCases,
        'Total deaths': obj_format.TotalDeaths,
        'New deaths': obj_format.NewDeaths,
        'Total recovered': obj_format.TotalRecovered,
        'New recovered': obj_format.NewRecovered,
        'Active cases': obj_format.ActiveCases,
        'Total tests': obj_format.TotalTests,
    }

    # obj_json = json.dumps(obj_format_dict, indent=2, ensure_ascii=False)
    #
    # for r in (("Global", "Весь мир"), ("Belarus", "Беларусь"), ("Russia", "Россия"), ("US", "США")):
    #     obj_json = obj_json.replace(*r)

    return Translator.trl_covid19_data(loc=args.localization, data=new_dict_resp)

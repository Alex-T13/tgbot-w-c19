from typing import Optional, List
from fastapi import status
from pydantic import Field
from pydantic.main import BaseModel

from config import settings
from custom_logging import logger


# class Cv19Data(BaseModel):
#     recovered: Optional[int] = Field(default=None)
#     deaths: Optional[int] = Field(default=None)
#     confirmed: Optional[int] = Field(default=None)
#     lastChecked: Optional[str] = Field(default=None)  # "2021-02-05T14:22:01+00:00",
#     lastReported: Optional[str] = Field(default=None)  # "2021-02-05T05:22:38+00:00",
#     location: str = Field(...)
#
#
# class Cv19Stat(BaseModel):
#     error: bool = Field(...)
#     statusCode: int = Field(...)
#     message: str = Field(...)
#     data: Cv19Data = Field(...)
# ---------------------------------------------
from localization.translator import Translator
from utils import FuncParameters


class Cv19Location(BaseModel):
    id: str = Field(...)
    rank: int = Field(...)
    Country: str = Field(...)
    Continent: str = Field(...)
    TwoLetterSymbol: Optional[str] = Field(default=None)
    ThreeLetterSymbol: Optional[str] = Field(default=None)
    Infection_Risk: int = Field(...)
    Case_Fatality_Rate: int = Field(...)
    Test_Percentage: int = Field(...)
    Recovery_Proporation: int = Field(...)
    TotalCases: int = Field(...)
    NewCases: int = Field(...)
    TotalDeaths: int = Field(...)
    NewDeaths: int = Field(...)
    TotalRecovered: str = Field(...)
    NewRecovered: int = Field(...)
    ActiveCases: int = Field(...)
    TotalTests: str = Field(...)
    Population: str = Field(...)
    one_Caseevery_X_ppl: int = Field(...)
    one_Deathevery_X_ppl: int = Field(...)
    one_Testevery_X_ppl: int = Field(...)
    Deaths_1M_pop: int = Field(...)
    Serious_Critical: int = Field(...)
    Tests_1M_Pop: int = Field(...)
    TotCases_1M_Pop: int = Field(...)


# class Cv19Data(BaseModel):
#     data: Optional[List[Cv19Location]] = Field(default=None)


async def covid19_data(args: FuncParameters) -> Optional[str]:
        # session: ClientSession, p_country: Optional[str] = None):
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

# import json
from typing import Optional
from aiohttp import ClientSession
from fastapi import status
from pydantic import Field
from pydantic.main import BaseModel
from custom_logging import logger


class Cv19Data(BaseModel):
    recovered_: int = Field(..., alias="Выздоровевших")
    deaths_: int = Field(..., alias="Умерших")
    confirmed_: int = Field(..., alias="Заболевших")
    lastChecked: Optional[str] = Field(default=None)  # "2021-02-05T14:22:01+00:00",
    lastReported: Optional[str] = Field(default=None)  # "2021-02-05T05:22:38+00:00",
    location_: str = Field(..., alias="Локация")


class Cv19Stat(BaseModel):
    error: bool = Field(...)
    statusCode: int = Field(...)
    message: str = Field(...)
    data: Cv19Data = Field(...)


# class Cv19Response(Cv19Data):
#     location: lo = Field(...)
#     confirmed = Field(...)
#     recovered = Field(...)
#     deaths = Field(...)

    # class Config:
    #     fields = {
    #         "location": "Локация",
    #         "confirmed": "Заболевших",
    #         "recovered": "Выздоровевших",
    #         "deaths": "Умерших",
    #     }


async def get_cv19_data(
        session: ClientSession, p_country: Optional[str] = None):  #  -> Optional[Cv19Data]:   # Optional[str]:
    if not p_country:
        url = "https://covid-19-coronavirus-statistics.p.rapidapi.com/v1/total"
    else:
        url = f"https://covid-19-coronavirus-statistics.p.rapidapi.com/v1/total?country={p_country}"
    headers = {
        'x-rapidapi-key': "8171e78a27mshe06f34e09766f70p1b5a9djsnf7011598a514",
        'x-rapidapi-host': "covid-19-coronavirus-statistics.p.rapidapi.com"
    }
    response = await session.get(url, headers=headers)

    if response.status != status.HTTP_200_OK:
        # print(response.status, response.text())
        logger.warning("telegram api call failed: %s", response)
        body = await response.text()
        logger.debug(body)

        return None

    print(f"{type(response)} из get_data_cv")

    payload = await response.json()

    print(f"{type(payload)} из get_data_cv payload")
    print(f"{payload} из get_data_cv payload")

    obj_format = Cv19Stat(**payload).data

    print(f"{type(obj_format)} из get_data_cv obj_format")
    print(f"{obj_format} из get_data_cv obj_format")

    # obj_format_2 = Cv19Data(**obj_format)

    obj_format_json = obj_format.json(exclude={'lastChecked', 'lastReported'}, by_alias=True)  # by_alias

    print(f"{type(obj_format_json)} из get_data_cv obj_format_json")
    print(f"{obj_format_json} из get_data_cv obj_format_json")

    # payload2 = Cv19Stat(payload)

    # res_dict = {
    #     "Локация": res_json['data']['location'],
    #     "Заболели": res_json['data']['confirmed'],
    #     "Выздоровели": res_json['data']['recovered'],
    #     "Умерли": res_json['data']['deaths'],
    # }
    # # payload = await res_dict.json()
    # payload = json.dumps(res_dict, indent=2, ensure_ascii=False)

    # print(payload)
    # payload = payload.dict(include={'confirmed', 'recovered', 'deaths', 'location'})
    return obj_format_json

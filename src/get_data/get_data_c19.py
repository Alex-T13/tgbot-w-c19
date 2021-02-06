# import json
from typing import Optional
from aiohttp import ClientSession
from fastapi import status
from pydantic import Field
from pydantic.main import BaseModel
from custom_logging import logger


class Cv19Data(BaseModel):
    confirmed: Optional[int] = Field(default=None, alias="Заболевших")  # 253413,
    recovered: Optional[int] = Field(default=None, alias="Выздоровевших")  # 241150,
    deaths: Optional[int] = Field(default=None, alias="Умерших")  # 1755,
    lastChecked: Optional[str] = Field(default=None)  # "2021-02-05T14:22:01+00:00",
    lastReported: Optional[str] = Field(default=None)  # "2021-02-05T05:22:38+00:00",
    location: Optional[str] = Field(default=None, alias="Локация")  # "Belarus"


class Cv19Stat(BaseModel):
    error: bool = Field(...)  # false,
    statusCode: int = Field(...)  # 200,
    message: str = Field(...)  # "OK",
    data: Optional[Cv19Data] = Field(default=None)


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
        session: ClientSession, p_country: Optional[str] = None) -> Optional[Cv19Stat]:
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

    # print(response.status)
    payload = await response.json()
    # payload = payload['data']

    # resp_cv19_dict = {
    #     "Локация": resp['data']['location'],
    #     "Заболели": resp['data']['confirmed'],
    #     "Выздоровели": resp['data']['recovered'],
    #     "Умерли": resp['data']['deaths'],
    # }
    # result = json.dumps(response, indent=2, ensure_ascii=False)

    # print(payload)
    # payload = payload.dict(include={'confirmed', 'recovered', 'deaths', 'location'})
    return payload

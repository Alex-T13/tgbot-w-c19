import json
from typing import Optional
from aiohttp import ClientSession
from fastapi import status
from pydantic import Field
from pydantic.main import BaseModel

from config import settings
from custom_logging import logger


class Cv19Data(BaseModel):
    recovered: Optional[int] = Field(default=None)
    deaths: Optional[int] = Field(default=None)
    confirmed: Optional[int] = Field(default=None)
    lastChecked: Optional[str] = Field(default=None)  # "2021-02-05T14:22:01+00:00",
    lastReported: Optional[str] = Field(default=None)  # "2021-02-05T05:22:38+00:00",
    location: str = Field(...)


class Cv19Stat(BaseModel):
    error: bool = Field(...)
    statusCode: int = Field(...)
    message: str = Field(...)
    data: Cv19Data = Field(...)


async def get_cv19_data(
        session: ClientSession, p_country: Optional[str] = None):
    if not p_country:
        url = "https://covid-19-coronavirus-statistics.p.rapidapi.com/v1/total"
    else:
        url = f"https://covid-19-coronavirus-statistics.p.rapidapi.com/v1/total?country={p_country}"
    headers = {
        'x-rapidapi-key': f"{settings.x_rapidapi_key}",
        'x-rapidapi-host': "covid-19-coronavirus-statistics.p.rapidapi.com"
    }
    response = await session.get(url, headers=headers)

    if response.status != status.HTTP_200_OK:
        logger.warning("covid-19-coronavirus api call failed: %s", response)
        body = await response.text()
        logger.debug(body)
        return None

    payload = await response.json()
    logger.debug(payload)

    obj_format = Cv19Stat(**payload).data

    obj_format_dict = {
        "Заболело": obj_format.confirmed,
        "Выздоровело": obj_format.recovered,
        "Умерло": obj_format.deaths,
        "Локация": obj_format.location,
    }
    obj_json = json.dumps(obj_format_dict, indent=2, ensure_ascii=False)

    for r in (("Global", "Весь мир"), ("Belarus", "Беларусь"), ("Russia", "Россия"), ("US", "США")):
        obj_json = obj_json.replace(*r)

    return obj_json

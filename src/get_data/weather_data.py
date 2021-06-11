import json
import inspect
from typing import Optional, List
from aiohttp import ClientSession
from fastapi import status
from pydantic import Field
from pydantic.main import BaseModel

from config import settings
from custom_logging import logger
from localization.translator import translator, Translator


class CoordW(BaseModel):
    lon: float = Field(...)
    lat: float = Field(...)


class Weather(BaseModel):
    id: int = Field(...)
    main: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)  # облачно
    icon: Optional[str] = Field(default=None)


class MainW(BaseModel):
    temp: int = Field(...)
    feels_like: float = Field(...)
    temp_min: int = Field(...)
    temp_max: int = Field(...)
    pressure: int = Field(...)
    humidity: int = Field(...)


class WindW(BaseModel):
    speed: Optional[int] = Field(default=None)
    deg: Optional[int] = Field(default=None)


class CloudsW(BaseModel):
    all: Optional[int] = Field(default=None)


class RainW(BaseModel):
    _1h: Optional[int] = Field(default=None)
    _3h: Optional[int] = Field(default=None)

    class Config:
        fields = {
            "_1h": "1h",
            "_3h": "3h",
        }


class SnowW(BaseModel):
    _1h: Optional[int] = Field(default=None)
    _3h: Optional[int] = Field(default=None)

    class Config:
        fields = {
            "_1h": "1h",
            "_3h": "3h",
        }


class SysW(BaseModel):
    type: Optional[int] = Field(default=None)
    id: int = Field(...)
    country: str = Field(...)
    sunrise: Optional[str] = Field(default=None)
    sunset: Optional[str] = Field(default=None)


class WeatherData(BaseModel):
    coord: Optional[CoordW] = Field(default=None)
    weather: List[Weather] = Field(default_factory=list)
    base: Optional[str] = Field(default=None)
    main: MainW = Field(...)
    visibility: Optional[int] = Field(default=None)
    wind: Optional[WindW] = Field(default=None)
    clouds: Optional[CloudsW] = Field(default=None)
    rain: Optional[RainW] = Field(default=None)
    snow: Optional[SnowW] = Field(default=None)
    dt: Optional[int] = Field(default=None)
    sys: SysW = Field(...)
    timezone: int = Field(...)
    id: int = Field(...)
    name: Optional[str] = Field(default=None)  # "Минск",
    cod: int = Field(...)


async def weather_data(session: ClientSession, loc: str) -> Optional[str]:
    # name = get_data_weather.__name__
    url = f"https://api.openweathermap.org/data/2.5/weather?id=625144&appid={settings.open_weather_appid}&units" \
          f"=metric&lang={loc}"
    response = await session.get(url)

    if response.status != status.HTTP_200_OK:
        logger.warning("openweathermap api call failed: %s", response)
        body = await response.text()
        logger.debug(body)

        return None

    resp_json = await response.json()
    resp_obj_format = WeatherData(**resp_json)

    new_dict_resp = {
        'city': resp_obj_format.name,
        'weather': resp_obj_format.weather[-1].description,
        'temperature(С)': resp_obj_format.main.temp,
        'feels like(C)': resp_obj_format.main.feels_like,
        'humidity(%)': resp_obj_format.main.humidity,
        'wind speed(m/s)': resp_obj_format.wind.speed,
        'cloudiness(%)': resp_obj_format.clouds.all
    }

    return Translator.trl_weather_data(loc=loc, data=new_dict_resp, )
    # return translator(loc=loc, data=new_dict_resp, )

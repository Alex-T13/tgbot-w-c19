import json
from typing import Optional
from typing import List
from aiohttp import ClientSession
from fastapi import status
from pydantic import Field
from pydantic.main import BaseModel

from config import settings
from custom_logging import logger


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


async def get_weather_data(session: ClientSession) -> Optional[str]:
    url = f"https://api.openweathermap.org/data/2.5/weather?id=625144&appid={settings.open_weather_appid}&units" \
          "=metric&lang=ru"
    response = await session.get(url)

    if response.status != status.HTTP_200_OK:
        logger.warning("openweathermap api call failed: %s", response)
        body = await response.text()
        logger.debug(body)

        return None

    payload = await response.json()
    obj_format = WeatherData(**payload)

    obj_format_dict = {
        "Город": obj_format.name,
        "Погодные условия": obj_format.weather[-1].description,
        "Температура(C)": obj_format.main.temp,
        "Ощущается(C)": obj_format.main.feels_like,
        "Влажность(%)": obj_format.main.humidity,
        "Скорость ветра(м/с)": obj_format.wind.speed,
        "Облачность(%)": obj_format.clouds.all
    }

    obj_json_str = json.dumps(obj_format_dict, indent=2, ensure_ascii=False)

    return obj_json_str

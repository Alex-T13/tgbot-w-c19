import json
from typing import Optional, List
from aiohttp import ClientSession
from fastapi import status
from pydantic import Field
from pydantic.main import BaseModel
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
    name: Optional[int] = Field(default=None)  # "Минск",
    cod: int = Field(...)


async def get_weather_data(session: ClientSession) -> Optional[str]:
    url = "https://api.openweathermap.org/data/2.5/weather?id=625144&appid=d8401dcbd228a0cecc87e84e2f65af62&units" \
          "=metric&lang=ru "

    response = await session.get(url)

    if response.status != status.HTTP_200_OK:
        # print(response.status, response.text())
        logger.warning("telegram api call failed: %s", response)
        body = await response.text()
        logger.debug(body)

        return None

    payload = await response.json()

    obj_format = WeatherData(**payload)

    print(f"{type(obj_format)} из get_data obj_format")
    print(f"{obj_format} из get_data obj_format")

    obj_format_dict = {
        "Город": obj_format.name,
        "Погодные условия": obj_format.weather[-1].description,
        "Температура(C)": obj_format.main.temp,
        "Ощущается(C)": obj_format.main.feels_like,
        "Влажность(%)": obj_format.main.humidity,
        "Скорость ветра(м/с)": obj_format.wind.speed,
        "Облачность": obj_format.clouds.all
    }

    obj_json_str = json.dumps(obj_format_dict, indent=2, ensure_ascii=False)

            # .json(include={"weather"., 'lastReported'})  # by_alias

    # for r in (("confirmed", "Заболело"), ("recovered", "Выздоровело"),
    #           ("deaths", "Умерло"), ("location", "Локация"), ("Global", "Весь мир"),
    #           ("Belarus", "Беларусь"), ("Russia", "Россия"), ("US", "США")):
    #     obj_json_str = obj_json_str.replace(*r)

    print(f"{obj_json_str} из get_data_cv obj_format_json")
    print(f"{type(obj_json_str)} из get_data_cv obj_format_json")

    return obj_json_str

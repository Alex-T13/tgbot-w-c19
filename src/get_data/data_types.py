import dataclasses
from typing import Optional, List, Union

from aiohttp import ClientSession
from pydantic import Field
from pydantic.main import BaseModel

from telegram.types import Message


# ------ weather_data ---------------------
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


# ------ covid19_data -------------
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
    TotalCases: str = Field(...)  # int
    NewCases: str = Field(...)  # int
    TotalDeaths: str = Field(...)  # int
    NewDeaths: str = Field(...)  # int
    TotalRecovered: str = Field(...)
    NewRecovered: str = Field(...)  # int
    ActiveCases: str = Field(...)  # int
    TotalTests: str = Field(...)
    Population: str = Field(...)
    one_Caseevery_X_ppl: int = Field(...)
    one_Deathevery_X_ppl: int = Field(...)
    one_Testevery_X_ppl: int = Field(...)
    Deaths_1M_pop: int = Field(...)
    Serious_Critical: int = Field(...)
    Tests_1M_Pop: int = Field(...)
    TotCases_1M_Pop: int = Field(...)


# ------------others----------------------------
@dataclasses.dataclass
class FuncParameters:
    localization: str
    session: Optional[ClientSession] = None
    message: Optional[Message] = None
    data: Optional[Union[dict, str]] = None

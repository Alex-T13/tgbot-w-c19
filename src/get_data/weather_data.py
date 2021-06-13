from typing import Optional
from fastapi import status

from config import settings
from custom_logging import logger
from get_data.data_types import WeatherData, FuncParameters
from localization.translator import Translator


async def weather_data(args: FuncParameters) -> Optional[str]:
    url = f"https://api.openweathermap.org/data/2.5/weather?id=625144&appid={settings.open_weather_appid}&units" \
          f"=metric&lang={args.localization}"
    response = await args.session.get(url)

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

    return Translator.data_translation(loc=args.localization, data=new_dict_resp)

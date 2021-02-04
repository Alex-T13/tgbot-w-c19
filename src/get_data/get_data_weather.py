import json
from typing import Optional
import requests


def get_weather_data(p_country: Optional[str] = None):  # -> Cv19StatData:  session: ClientSession
    url = "https://api.openweathermap.org/data/2.5/weather"
    querystring = {
        "id": 625144,
        "appid": "d8401dcbd228a0cecc87e84e2f65af62",
        "units": "metric",
        "lang": "ru",
    }
    resp = requests.get(url, params=querystring)

    if resp.status_code != 200:
        return f"response content error: {resp.text}"
    resp = resp.json()

    resp_weather_dict = {
    #     "Локация": resp['data']['location'],
    #     "Заболели": resp['data']['confirmed'],
    #     "Выздоровели": resp['data']['recovered'],
    #     "Умерли": resp['data']['deaths'],
    # }
    # result = json.dumps(resp_cv19_dict, indent=2, ensure_ascii=False)
    # print(result)
    return result


# country = "Belarus"
#
#
# get_cv19_data(country)
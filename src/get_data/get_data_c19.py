import json
from typing import Optional

import requests


def get_cv19_data(p_country: Optional[str] = None):  # -> Cv19StatData:
    url = "https://covid-19-coronavirus-statistics.p.rapidapi.com/v1/total"
    querystring = {"country": p_country}
    headers = {
        'x-rapidapi-key': "8171e78a27mshe06f34e09766f70p1b5a9djsnf7011598a514",
        'x-rapidapi-host': "covid-19-coronavirus-statistics.p.rapidapi.com"
    }
    resp = requests.get(url, headers=headers, params=querystring).json()
    resp_cv19_dict = {
        "Локация": resp['data']['location'],
        "Заболели": resp['data']['confirmed'],
        "Выздоровели": resp['data']['recovered'],
        "Умерли": resp['data']['deaths'],
    }
    result = json.dumps(resp_cv19_dict, indent=4, ensure_ascii=False)
    # print(result)
    return result


# country = "Belarus"
#
#
# get_cv19_data(country)

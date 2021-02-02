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
    result = resp   # json(indent=2, sort_keys=True)
    print(resp_cv19_dict)
    return resp_cv19_dict


country = "Belarus"


get_cv19_data(country)
# print("смертей: ", get_cv19_data(country))


# async def main():
#
#     async with aiohttp.ClientSession() as session:
#         async with session.get('http://python.org') as response:
#
#             print("Status:", response.status)
#             print("Content-type:", response.headers['content-type'])
#
#             html = await response.text()
#             print("Body:", html[:15], "...")
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())


# if __name__ == "__main__":
#     import uvicorn
#
#     uvicorn.run(app, host="0.0.0.0", port=PORT)

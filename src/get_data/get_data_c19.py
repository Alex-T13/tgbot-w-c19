import json
from typing import Optional

import requests
from aiohttp import ClientSession

from aiohttp import ClientSession
from fastapi import Depends
from fastapi import FastAPI
from fastapi import Form
from fastapi import HTTPException
from fastapi import Request
from fastapi import status


# async def index(
#     request: Request,
#     # client_session: ClientSession = Depends(http_client_session),
# ):
#     logger.debug("handling index")
#     webhook = await get_webhook_info(client_session)
#     context = {
#         "path_setup_webhook": PATH_SETUP_WEBHOOK,
#         "url_webhook_current": hide_webhook_token(webhook.url if webhook else "not set"),
#         "url_webhook_new": hide_webhook_token(URL_WEBHOOK),
#     }
#
#     response = templates.TemplateResponse("index.html", {"request": request, **context})
#
#     return response
#
#
# async def get_webhook_info(session: ClientSession, /) -> Optional[WebhookInfo]:
#     result = await _call_tg_method(session, "getWebhookInfo")
#     webhook_info = WebhookInfo.parse_obj(result)
#
#     return webhook_info
#
#
# async def _call_tg_method(session: ClientSession, method_name: str, /, **kw):
#     url = f"{URL_TELEGRAM_API}/{method_name}"
#     response = await session.post(url, **kw)
#     if response.status != status.HTTP_200_OK:
#         logger.warning("telegram api call failed: %s", response)
#         body = await response.text()
#         logger.debug(body)
#
#         return None
#
#     payload = await response.json()
#     if not (ok := payload.get("ok")):
#         logger.warning("payload is not ok: %s", ok)
#         logger.debug(payload)
#
#         return None
#
#     result = payload["result"]
#     return result


# async def http_client_session():
#     async with ClientSession() as session:
#         yield session
from custom_logging import logger


async def get_cv19_data(session: ClientSession,  # = Depends(http_client_session),
                        p_country: Optional[str] = None):  # -> Cv19StatData:
    # url = "https://covid-19-coronavirus-statistics.p.rapidapi.com/v1/total"
    url = f"https://covid-19-coronavirus-statistics.p.rapidapi.com/v1/total?country={p_country}"
    # querystring = {"country": p_country}
    headers = {
        'x-rapidapi-key': "8171e78a27mshe06f34e09766f70p1b5a9djsnf7011598a514",
        'x-rapidapi-host': "covid-19-coronavirus-statistics.p.rapidapi.com"
    }
    response = await session.get(url, headers=headers)
    # async with session.get(url, headers=headers) as response:
    # resp = await requests.get(url, headers=headers, params=querystring)

    if response.status != status.HTTP_200_OK:
        print(response.status, response.text())
        logger.warning("telegram api call failed: %s", response)
        body = await response.text()
        logger.debug(body)

        return None
    # if resp.status_code != 200:
    #     return f"response content error: {resp.text}"
    #     logger.warning("rapidapi.com api call failed: %s", resp)
    #     body = resp.text
    #     logger.debug(body)
    payload = json.dumps(response, indent=2, ensure_ascii=False)  # await response.json()

    # resp_cv19_dict = {
    #     "Локация": resp['data']['location'],
    #     "Заболели": resp['data']['confirmed'],
    #     "Выздоровели": resp['data']['recovered'],
    #     "Умерли": resp['data']['deaths'],
    # }
    # result = json.dumps(resp_cv19_dict, indent=2, ensure_ascii=False)
    print(payload)
    return payload


# country = "Belarus"
#
# get_cv19_data(ClientSession, country)



# async def get_cv19_data(session: ClientSession, p_country: Optional[str] = None):  # -> Cv19StatData:
#     url = "https://covid-19-coronavirus-statistics.p.rapidapi.com/v1/total"
#     querystring = {"country": p_country}
#     headers = {
#         'x-rapidapi-key': "8171e78a27mshe06f34e09766f70p1b5a9djsnf7011598a514",
#         'x-rapidapi-host': "covid-19-coronavirus-statistics.p.rapidapi.com"
#     }
#     resp = await requests.get(url, headers=headers, params=querystring)
#
#     if resp.status_code != 200:
#         return f"response content error: {resp.text}"
#     #     logger.warning("rapidapi.com api call failed: %s", resp)
#     #     body = resp.text
#     #     logger.debug(body)
#     resp = resp.json()
#
#     resp_cv19_dict = {
#         "Локация": resp['data']['location'],
#         "Заболели": resp['data']['confirmed'],
#         "Выздоровели": resp['data']['recovered'],
#         "Умерли": resp['data']['deaths'],
#     }
#     result = json.dumps(resp_cv19_dict, indent=2, ensure_ascii=False)
#     # print(result)
#     return result
#
#


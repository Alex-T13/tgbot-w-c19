import json

from aiohttp import ClientSession
from fastapi import status
from custom_logging import logger


async def get_currency(session: ClientSession, ):

    url = f"https://www.nbrb.by/api/exrates/rates?periodicity=0"

    response = await session.get(url)

    if response.status != status.HTTP_200_OK:
        logger.warning("www.nbrb.by api call failed: %s", response)
        body = await response.text()
        logger.debug(body)

        return None

    payload = await response.json()

    cur_dict = {
        "Доллар США": 145,
        "Евро": 292,
        "100 Российских рублей": 298,
        "Украинская гривна": 290,
    }

    for key in cur_dict:
        cur_filter = list(filter(lambda cur: cur['Cur_ID'] == cur_dict.get(key), payload))[-1]['Cur_OfficialRate']
        cur_dict[key] = cur_filter

    obj_json_str = json.dumps(cur_dict, indent=2, ensure_ascii=False)

    return obj_json_str


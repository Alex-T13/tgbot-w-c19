import json

from aiohttp import ClientSession
from fastapi import status
from custom_logging import logger


async def get_btc(session: ClientSession, ):

    url = "https://apirone.com/api/v2/ticker?currency=btc"

    response = await session.get(url)

    if response.status != status.HTTP_200_OK:
        logger.warning("https://apirone.com api call failed: %s", response)
        body = await response.text()
        logger.debug(body)

        return None

    btc = await response.json()
    logger.debug(f"get btc in response: {btc}")

    btc_str = f"Курс биткойна к USD: {btc['usd']}"

    obj_json_str = json.dumps(btc_str, indent=2, ensure_ascii=False)

    return obj_json_str

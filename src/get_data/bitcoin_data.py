from typing import Optional

from fastapi import status
from custom_logging import logger
from get_data.data_types import FuncParameters
from localization.translator import Translator


async def bitcoin_data(args: FuncParameters) -> Optional[str]:
    url = "https://apirone.com/api/v2/ticker?currency=btc"
    response = await args.session.get(url)
    if response.status != status.HTTP_200_OK:
        logger.warning("https://apirone.com api call failed: %s", response)
        body = await response.text()
        logger.debug(body)
        return None

    payload = await response.json()
    new_dict_resp = {
        'USD': payload['usd']
    }

    return Translator.data_translation(loc=args.localization, data=new_dict_resp)

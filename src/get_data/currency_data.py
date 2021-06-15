from typing import Optional

from fastapi import status
from custom_logging import logger
from get_data.data_types import FuncParameters
from localization.translator import Translator


async def currency_data(args: FuncParameters) -> Optional[str]:
    url = f"https://www.nbrb.by/api/exrates/rates?periodicity=0"
    response = await args.session.get(url)
    if response.status != status.HTTP_200_OK:
        logger.warning("www.nbrb.by api call failed: %s", response)
        body = await response.text()
        logger.debug(body)
        return None

    payload = await response.json()
    new_dict_resp = {
        'USD': 145,
        'EUR': 292,
        '100 RUB': 298,
        '100 UAH': 290,
        '10 PLN': 293,
    }

    for key in new_dict_resp:
        curr_filter = list(filter(lambda cur: cur['Cur_ID'] == new_dict_resp.get(key), payload))[-1]['Cur_OfficialRate']
        new_dict_resp[key] = curr_filter

    return Translator.data_translation(loc=args.localization, data=new_dict_resp)


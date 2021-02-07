import json

from aiohttp import ClientSession
from fastapi import status
from custom_logging import logger


async def get_currency(session: ClientSession, ):

    url = f"https://www.nbrb.by/api/exrates/rates?periodicity=0"

    response = await session.get(url)

    if response.status != status.HTTP_200_OK:
        # print(response.status, response.text())
        logger.warning("telegram api call failed: %s", response)
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
        # print(cur_dict[key])
        cur_filter = list(filter(lambda cur: cur['Cur_ID'] == cur_dict.get(key), payload))[-1]['Cur_OfficialRate']
        # print(cur_filter)
        # print(cur_filter[-1]['Cur_OfficialRate'])
        cur_dict[key] = cur_filter

    obj_json_str = json.dumps(cur_dict, indent=2, ensure_ascii=False)

    # print(f"{obj_json_str} из get_data_cv obj_format_json")
    # print(f"{type(obj_json_str)} из get_data_cv obj_format_json")

    return obj_json_str


# get
#
# ondate** – дата, на которую запрашивается курс (если не задана, то возвращается курс на сегодня)
# periodicity – периодичность установления курса (0 – ежедневно, 1 – ежемесячно)
# parammode – формат аргумента cur_id: 0 – внутренний код валюты, 1 – трехзначный цифровой  код валюты
#     в соответствии со стандартом ИСО 4217, 2 – трехзначный буквенный код валюты (ИСО 4217). По умолчанию = 0

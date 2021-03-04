from datetime import datetime, timedelta
from typing import Optional
from aiohttp import ClientSession

from custom_logging import logger
from db.crud import get_last_message
from get_data.get_currency import get_currency
from get_data.get_data_c19 import get_cv19_data
from get_data.get_data_weather import get_weather_data
from telegram.types import Message


async def main_switch_update(update_massage: Message, session: ClientSession):
    if update_massage.entities:
        bot_command = True if update_massage.entities[-1].type == "bot_command" else False  # maybe through: list(filter(lambda
        if bot_command:
            allowed_list = ("/weather", "/currency", "/covid19global", "/covid19blr", "/covid19rus", "/covid19usa")
            if update_massage.text not in allowed_list:
                return choice_of_answer("")

            return await select_command_action(session, update_massage.text)

    switch_dict = {
        "text": lambda: choice_of_answer(update_massage.text),
        "animation": lambda: choice_of_answer(""),
        "sticker": lambda: choice_of_answer(""),
        "voice": lambda: choice_of_answer(""),
    }

    for key, value in update_massage.dict().items():
        if key in switch_dict and value:

            return switch_dict[key]()

    return "Не шли мне такое, я не знаю что с этим делать."


def choice_of_answer(ar: Optional[str] = None):
    check1 = ["hi", "hello", "good morning", "good afternoon", "good evening", "привет", "здравствуй", "здравствуйте",
              "доброе утро", "добрый день", "добрый вечер"]
    check2 = ["дай ответ на главный вопрос жизни, вселенной и вообще",
              "give an answer to the ultimate question of life, the universe, and everything"]
    if ar.lower() in check1:
        return ar
    elif ar.lower() in check2:
        return "42"
    else:
        return "Ok"


def select_command_action(session: ClientSession, arg: str):
    switcher = {
        "/weather": lambda: get_weather_data(session),
        "/currency": lambda: get_currency(session),
        "/covid19global": lambda: get_cv19_data(session),
        "/covid19blr": lambda: get_cv19_data(session, "Belarus"),
        "/covid19rus": lambda: get_cv19_data(session, "Russia"),
        "/covid19usa": lambda: get_cv19_data(session, "USA"),
    }
    payload = switcher[arg]()
    return payload


async def get_last_msg(msg: Message, ):
    l_msg = get_last_message(msg.from_.id)
    logger.debug(f"get_last_message: {l_msg}")

    since = datetime.now() - timedelta(seconds=10)
    return True if l_msg.created_at < since else False

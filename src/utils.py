from typing import Optional
from aiohttp import ClientSession

from get_data.get_currency import get_currency
from get_data.get_data_c19 import get_cv19_data
from get_data.get_data_weather import get_weather_data
from telegram.types import Message


async def main_switch_update(update_massage: Message, session: ClientSession):

    if update_massage.entities:
        bot_command = True if update_massage.entities[-1].type == "bot_command" else False  # maybe through: list(filter(lambda
        if bot_command:
            if update_massage.text == "/start":
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

    return "Keys not found"


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

    # try:
    #     return switcher[arg]()   #######doesn't work###############
    # except ValueError:
    #
    #     print("Не верный параметр bot-command")
    #
    #     return "Не верный параметр bot-command"

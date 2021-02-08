from typing import Dict, Optional
from aiohttp import ClientSession

from get_data.get_currency import get_currency
from get_data.get_data_c19 import get_cv19_data
from get_data.get_data_weather import get_weather_data


def main_switch_update(session: ClientSession, update_mass):
    switch_dict = {
        "update_mass.entities": lambda: select_event(session, update_mass.text),
        "update_mass.text": lambda: choice_of_answer(update_mass.text),
        "update_mass.animation": lambda: choice_of_answer(""),
        "update_mass.sticker": lambda: choice_of_answer(""),
        "update_mass.voice": lambda: choice_of_answer(""),
    }

    for key in switch_dict:
        if switch_dict[key] in update_mass is not None:
            return switch_dict[key]()


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


def select_event(session: ClientSession, arg: str):
    switcher = {
        "/weather": lambda: get_weather_data(session),
        "/currency": lambda: get_currency(session),
        "/covid19global": lambda: get_cv19_data(session),
        "/covid19blr": lambda: get_cv19_data(session, "Belarus"),
        "/covid19rus": lambda: get_cv19_data(session, "Russia"),
        "/covid19usa": lambda: get_cv19_data(session, "USA"),
    }

    try:
        return switcher[arg]()
    except ValueError:
        return "Не верный параметр bot-command"

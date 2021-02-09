from typing import Dict, Optional
from aiohttp import ClientSession

from get_data.get_currency import get_currency
from get_data.get_data_c19 import get_cv19_data
from get_data.get_data_weather import get_weather_data
from telegram.types import Update, Message


def main_switch_update(session: ClientSession, update_massage: Message):

    print(f"{update_massage}  This is update_massage")

    update = update_massage.dict()

    print(f"{update}  This is update")

    switch_dict = {
        "entities": lambda: await select_event(session, update['text']),
        "text": lambda: choice_of_answer(update['text']),
        "animation": lambda: choice_of_answer(""),
        "sticker": lambda: choice_of_answer(""),
        "voice": lambda: choice_of_answer(""),
    }
    print(f"{update_massage.text}  This is update_massage.text")
    print(f"{update['text']}  This is update['text']")

    # print(update_mass)

    for key in switch_dict:
        if key in update:
            print(f"{update[key]}  This is update[key] in if")

            if update[key]:

                print(key)
                print(type(key))
                print(update[key])

                return switch_dict[key]()
            else:
                print("key value is None")
                # return "key value is None"
        else:
            print(key)
            # return "Keys not found"

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

        print("Не верный параметр bot-command")

        return "Не верный параметр bot-command"

from typing import Dict, Optional
from aiohttp import ClientSession

from get_data.get_currency import get_currency
from get_data.get_data_c19 import get_cv19_data
from get_data.get_data_weather import get_weather_data
from telegram.types import Update, Message


# async def main_switch_update1(session: ClientSession, update_massage: Message):
#     # update = update_massage
#     update = update_massage.dict()
#
#     switch_dict = {
#         "entities": lambda: await select_event(session, update_massage.text),
#         "text": lambda: choice_of_answer(update_massage.text),  # update['text']
#         "animation": lambda: choice_of_answer(""),
#         "sticker": lambda: choice_of_answer(""),
#         "voice": lambda: choice_of_answer(""),
#     }
#
#     return switch_dict[key]()
#
#     for key in switch_dict:
#         if update[key] is not None:
#
#     print([x for x in my_data if x])


async def main_switch_update(session: ClientSession, update: Update):
    print(f"{update}  This is update")

    update_massage = update.message if update.message is not None else update.edited_message
    print(f"{update}  This is update_massage")
    bot_command = True if update_massage.entities[-1].type == "bot_command" else False
    # maybe through: list(filter(lambda

    if bot_command:
        await select_command_action(session, update_massage.text)

    switch_dict = {
        "text": lambda: choice_of_answer(update_massage.text),  # update['text']
        "animation": lambda: choice_of_answer(""),
        "sticker": lambda: choice_of_answer(""),
        "voice": lambda: choice_of_answer(""),
    }
    print(f"{update_massage.text}  This is update_massage.text")
    # print(f"{update['text']}  This is update['text']")

    # print(update_mass)

    for key, value in update_massage.dict().items():
        if value:
            print(f"{value},  {key}     This is key, value in if")

            return switch_dict[key]()
        else:
            print(key)
            print("key is None")

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

    try:
        return switcher[arg]()   ###########################################
    except ValueError:

        print("Не верный параметр bot-command")

        return "Не верный параметр bot-command"

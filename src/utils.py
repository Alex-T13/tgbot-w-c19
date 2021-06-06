from datetime import datetime, timedelta
from typing import Optional
from aiohttp import ClientSession

from custom_logging import logger
from db.crud import get_last_message
from get_data.get_btc import get_btc
from get_data.get_currency import get_currency
from get_data.get_data_c19 import get_cv19_data
from get_data.get_data_weather import get_weather_data
from telegram.methods import send_message
from telegram.types import Message


async def main_switch_update(session: ClientSession, update_massage: Message, ):
    if update_massage.entities:
        bot_command = True if update_massage.entities[-1].type == "bot_command" else False   # !!!!warning!!!
        if bot_command:
            allowed_list = ("/weather", "/currency", "/btc", "/covid19global", "/covid19blr", "/covid19rus", "/covid19usa")
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
        "/weather": lambda: get_weather_data(session),  # !асинхронный запуск должен быть
        "/currency": lambda: get_currency(session),
        "/btc": lambda: get_btc(session),
        "/covid19global": lambda: get_cv19_data(session),
        "/covid19blr": lambda: get_cv19_data(session, "Belarus"),
        "/covid19rus": lambda: get_cv19_data(session, "Russia"),
        "/covid19usa": lambda: get_cv19_data(session, "USA"),
    }
    payload = switcher[arg]()
    return payload


async def welcome_back(session: ClientSession, message: Message, ):
    last_message = get_last_message(message.from_.id)
    logger.debug(f"last message: {last_message}")
    # logger.debug(last_message.json(indent=2, sort_keys=True))
    since = datetime.now() - timedelta(minutes=1)  # 30/ 12hours

    if last_message.created_at < since:
        await send_message(session, chat_id=message.chat.id, text=f"С возвращением {message.from_.first_name}!")
        logger.debug(f"the message 'welcome back' was sent to the user: {message.from_.first_name}, "
                     f"id: {message.from_.id}")

    return None

from datetime import datetime, timedelta
from typing import Optional
from aiohttp import ClientSession

from custom_logging import logger
from db.crud import get_last_message
from get_data.bitcoin_data import get_data_btc
from get_data.currency_data import get_data_currency
from get_data.covid19_data import get_data_cv19
from get_data.weather_data import get_data_weather
from telegram.methods import send_message
from telegram.types import Message


VALID_BOT_COMMANDS = {
        "/weather": lambda: get_data_weather,              # session!!
        "/currency": lambda: get_data_currency,
        "/btc": lambda: get_data_btc,
        "/covid19global": lambda: get_data_cv19,
        "/covid19blr": lambda: get_data_cv19,   # session ,"Belarus"
        "/covid19rus": lambda: get_data_cv19,    # session, "Russia"
        "/covid19usa": lambda: get_data_cv19,       # session, "USA"
}

# a = VALID_BOT_COMMANDS.keys()
# b = VALID_BOT_COMMANDS.get()

# choices = {'a': 1, 'b': 2}
# result = choices.get(key, 'default')


# option = number['type']
# result = {
#     'number':     value_of_int,  # result = value_of_int(number['value'])
#     'text':       value_of_text, # result = value_of_text(number['value'])
#     'binary':     value_of_bin,  # result = value_of_bin(number['value'])
# }.get(option)(value['value'])


async def choice_of_answer(session: ClientSession, update_massage: Message, ):
    if update_massage.entities:
        return await if_bot_command(session, update_massage)

    try:
        payload = message_type_handler(update_massage).title()
    except AttributeError:
        return "Не шли мне такое, я не знаю что с этим делать."    #обратиться к функ. "переводчик" с параметром choice_of_answer
    else:
        return payload


def choice_of_greeting(arg="Ok") -> str:
    check1 = ["hi", "hello", "good morning", "good afternoon", "good evening", "привет", "здравствуй", "здравствуйте",
              "доброе утро", "добрый день", "добрый вечер"]
    check2 = ["дай ответ на главный вопрос жизни, вселенной и вообще",
              "give an answer to the ultimate question of life, the universe, and everything"]
    if arg.lower() in check1:
        return arg
    elif arg.lower() in check2:
        return "42"
    else:
        return "Ok"


async def select_command_action(session: ClientSession, arg: str) -> str:
    switcher = {
        "/weather": lambda: get_data_weather(session),
        "/currency": lambda: get_data_currency(session),
        "/btc": lambda: get_data_btc(session),
        "/covid19global": lambda: get_data_cv19(session),
        "/covid19blr": lambda: get_data_cv19(session, "Belarus"),
        "/covid19rus": lambda: get_data_cv19(session, "Russia"),
        "/covid19usa": lambda: get_data_cv19(session, "USA"),
    }
    payload = await switcher[arg]()
    return payload


async def welcome_back(session: ClientSession, message: Message, ):
    last_message = get_last_message(message.from_.id)
    logger.debug(f"last message: {last_message}")
    since = datetime.now() - timedelta(minutes=5)  # 30/ 12hours

    if last_message.created_at < since:
        await send_message(session, chat_id=message.chat.id, text=f"С возвращением {message.from_.first_name}!")
        logger.debug(f"the message 'welcome back' was sent to the user: {message.from_.first_name}, "
                     f"id: {message.from_.id}")

    return None


async def if_bot_command(session: ClientSession, update_massage: Message) -> Optional[str]:
    for att in update_massage.entities:
        logger.debug(f"entities: {att}")
        if att.type == "bot_command":
            logger.debug(f"This is a bot command - {update_massage.text}")
            if update_massage.text in VALID_BOT_COMMANDS.keys():
                return await select_command_action(session, update_massage.text)
    logger.debug("This is not a bot command")
    return choice_of_greeting()


def message_type_handler(update_massage: Message) -> Optional[str]:
    message_type = {
        "text": lambda: choice_of_greeting(update_massage.text),
        "animation": lambda: choice_of_greeting(),
        "sticker": lambda: choice_of_greeting(),
    }
    payload = ""
    for key, value in update_massage.dict().items():
        if key in message_type and value:  # value == True
            logger.debug(f"message_type - {key}")
            payload = message_type[key]()
            break
    logger.debug(f"payload - {payload if payload else 'None'}")
    return payload if payload else None

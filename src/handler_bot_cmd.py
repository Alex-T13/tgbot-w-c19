from typing import Optional

from custom_logging import logger
from get_data.bitcoin_data import bitcoin_data
from get_data.currency_data import currency_data
from get_data.covid19_data import covid19_data
from get_data.data_types import FuncParameters
from get_data.weather_data import weather_data
from localization import vocabularies
from localization.translator import Translator
from utils import language

VALID_BOT_COMMANDS = {
        '/weather': weather_data,
        '/currency': currency_data,
        '/btc': bitcoin_data,
        '/cv19belarus': covid19_data,
        '/cv19world': covid19_data,
        '/ru': language,
        '/en': language,
}


async def choice_of_answer(args: FuncParameters) -> str:
    if args.message.entities:
        return await if_bot_command(args)
    try:
        payload = message_type_handler(args)
        if not payload:
            raise AttributeError
    except AttributeError:
        return Translator.trl_choice_of_answer(loc=args.localization, data=args.message.from_.first_name)
    else:
        return payload


def choice_of_greeting(args: FuncParameters) -> str:
    if args.message.text.title() in vocabularies.CHOICE_OF_GREETING[args.localization]:
        return args.message.text.title()
    elif args.message.text.capitalize() == vocabularies.CHOICE_OF_ANSWER_EEGG.get(args.localization):
        return "42"
    else:
        return "Ok"


async def running_bot_command(args: FuncParameters) -> str:
    func = VALID_BOT_COMMANDS.get(args.message.text)

    lang = ['/ru', '/en']
    if args.message.text in lang:
        payload = func(args)
    else:
        payload = await func(args)
    return payload


async def if_bot_command(args: FuncParameters) -> Optional[str]:
    for attr in args.message.entities:
        if attr.type == "bot_command":
            logger.debug(f"This is a bot command - {args.message.text}")
            if args.message.text in VALID_BOT_COMMANDS.keys():
                return await running_bot_command(args)
    return choice_of_greeting(args)


def message_type_handler(args: FuncParameters) -> Optional[str]:
    message_type = {
        "text": choice_of_greeting,
        "animation": choice_of_greeting,
        "sticker": choice_of_greeting,
    }
    payload = ""
    for key, value in args.message.dict().items():
        if key in message_type and value:  # value == True
            logger.debug(f"message_type - {key}")
            payload = message_type[key](args)
            break
    logger.debug(f"payload - {payload if payload else 'None'}")
    return payload if payload else None

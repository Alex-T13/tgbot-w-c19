from datetime import datetime, timedelta

from custom_logging import logger
from db.crud import get_last_message, set_language
from get_data.data_types import FuncParameters
from localization import vocabularies
from localization.translator import Translator


async def welcome_back(args: FuncParameters) -> str:
    last_message = get_last_message(args.message.from_.id)
    since = datetime.now() - timedelta(hours=3)

    if last_message and last_message.created_at < since:
        logger.debug(f"the message 'welcome back' will be sent to user: {args.message.from_.first_name}, "
                     f"id: {args.message.from_.id}")
        return Translator.trl_welcome_back(loc=args.localization, data=args.message.from_.first_name)


def language_info() -> str:
    text = f"{vocabularies.LANGUAGE_INFO['ru']}   {vocabularies.LANGUAGE_INFO['en']}"
    return text


def language(args: FuncParameters) -> str:
    if args.localization == args.message.text[1:]:
        text = f"{vocabularies.SET_LANGUAGE[args.localization]}"
    else:
        text = f"{vocabularies.SET_LANGUAGE[set_language(args)]}"
        logger.debug(f"{text}")
    return text

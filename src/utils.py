from datetime import datetime, timedelta

from custom_logging import logger
from db.crud import get_last_message
from get_data.data_types import FuncParameters
from localization.translator import Translator


async def welcome_back(args: FuncParameters) -> str:
    last_message = get_last_message(args.message.from_.id)
    since = datetime.now() - timedelta(minutes=30)  # 30/ 12hours

    if last_message.created_at < since:
        logger.debug(f"the message 'welcome back' will be sent to user: {args.message.from_.first_name}, "
                     f"id: {args.message.from_.id}")
        return Translator.trl_welcome_back(loc=args.localization, data=args.message.from_.first_name)



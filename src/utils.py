import dataclasses
from datetime import datetime, timedelta
from typing import Optional, Union

from aiohttp import ClientSession

from custom_logging import logger
from db.crud import get_last_message
from localization.translator import Translator
from telegram.types import Message


@dataclasses.dataclass
class FuncParameters:

    localization: str
    # text: Optional[str] = None
    session: Optional[ClientSession] = None
    message: Optional[Message] = None
    data: Optional[Union[dict, str]] = None


# class ResponseT(NamedTuple):
#     status: str
#     headers: Optional[dict] = None
#     payload: Optional[bytes] = None


async def welcome_back(args: FuncParameters) -> str:
    last_message = get_last_message(args.message.from_.id)
    since = datetime.now() - timedelta(minutes=30)  # 30/ 12hours

    if last_message.created_at < since:
        logger.debug(f"the message 'welcome back' will be sent to user: {args.message.from_.first_name}, "
                     f"id: {args.message.from_.id}")
        return Translator.trl_welcome_back(loc=args.localization, data=args.message.from_.first_name)



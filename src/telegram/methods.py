from typing import Optional
from typing import Union

from aiohttp import ClientSession
from fastapi import status

from custom_logging import logger
from telegram.types import Message
from telegram.types import WebhookInfo
from urls import URL_TELEGRAM_API


# from src.custom_logging import logger
# from src.telegram.types import Message
# from src.telegram.types import WebhookInfo
# from src.urls import URL_TELEGRAM_API


async def get_webhook_info(session: ClientSession, /) -> Optional[WebhookInfo]:
    result = await _call_tg_method(session, "getWebhookInfo")
    webhook_info = WebhookInfo.parse_obj(result)

    return webhook_info


async def set_webhook(
    session: ClientSession,
    /,
    *,
    webhook_url: str,
) -> bool:
    data = {
        "url": webhook_url,
    }

    result = await _call_tg_method(session, "setWebhook", json=data)
    return result


async def send_message(
    session: ClientSession,
    /,
    *,
    chat_id: Union[str, int],
    text: str,
) -> Optional[Message]:
    data = {
        "chat_id": chat_id,
        "text": text,
    }

    result = await _call_tg_method(session, "sendMessage", json=data)
    message = Message.parse_obj(result)

    return message


async def _call_tg_method(session: ClientSession, method_name: str, /, **kw):
    url = f"{URL_TELEGRAM_API}/{method_name}"
    response = await session.post(url, **kw)
    if response.status != status.HTTP_200_OK:
        logger.warning("telegram api call failed: %s", response)
        body = await response.text()
        logger.debug(body)

        return None

    payload = await response.json()
    if not (ok := payload.get("ok")):
        logger.warning("payload is not ok: %s", ok)
        logger.debug(payload)

        return None

    result = payload["result"]
    return result

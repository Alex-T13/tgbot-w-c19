import json

from aiohttp import ClientSession
from fastapi import Depends
from fastapi import FastAPI
from fastapi import Form
from fastapi import HTTPException
from fastapi import Request
from fastapi import status
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from config import settings
from custom_logging import logger
from dirs import DIR_TEMPLATES
from telegram.methods import get_webhook_info
from telegram.methods import send_message
from telegram.methods import set_webhook
from telegram.types import Update
from urls import hide_webhook_token
from urls import PATH_DOCS
from urls import PATH_ROOT
from urls import PATH_SETUP_WEBHOOK
from urls import PATH_WEBHOOK_SECRET
from urls import URL_WEBHOOK
from urls import URL_WEBHOOK_SECRET
from utils import choice_of_answer
from utils import select_event_of_command


app = FastAPI(
    description="Telegram Bot",
    docs_url=f"{PATH_DOCS}/",
    openapi_url=f"{PATH_DOCS}/openapi.json",
    redoc_url=f"{PATH_DOCS}/redoc/",
    title="Telegram Bot API",
    version="1.0.0",
)

templates = Jinja2Templates(directory=DIR_TEMPLATES)


async def http_client_session():
    async with ClientSession() as session:
        yield session


@app.get(f"{PATH_ROOT}/", response_class=HTMLResponse)
async def index(
    request: Request,
    client_session: ClientSession = Depends(http_client_session),
):
    logger.debug("handling index")
    webhook = await get_webhook_info(client_session)
    context = {
        "path_setup_webhook": PATH_SETUP_WEBHOOK,
        "url_webhook_current": hide_webhook_token(webhook.url if webhook else "not set"),
        "url_webhook_new": hide_webhook_token(URL_WEBHOOK),
    }

    response = templates.TemplateResponse("index.html", {"request": request, **context})

    return response


@app.post(f"{PATH_SETUP_WEBHOOK}/")
async def handle_setup_webhook(
    password: str = Form(...),
    client_session: ClientSession = Depends(http_client_session),
):
    if password != settings.admin_password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin is allowed to configure webhook",
        )

    webhook_set = await set_webhook(client_session, webhook_url=f"{URL_WEBHOOK_SECRET}/",)
    if not webhook_set:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="webhook was not set",
        )

    return RedirectResponse(
        f"{PATH_ROOT}/",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@app.post(f"{PATH_WEBHOOK_SECRET}/")
async def handle_webhook(update: Update, client_session: ClientSession = Depends(http_client_session),):
    update_massage = update.message if update.message is not None else update.edited_message
    if not update_massage.entities:
        # print(f"{update_massage} entities is None")
        answer = choice_of_answer(update_massage.text)
    else:
        # print(f"{update_massage} entities is try")
        answer = await select_event_of_command(client_session, update_massage.text)
        answer.dict()
        # answer = answer.dict(include={'confirmed', 'recovered', 'deaths', 'location'})
        # answer = json.dumps(answer, indent=2, ensure_ascii=False,)
        # print(f"{answ} entities is try")
    # text = update.json(indent=4, sort_keys=True)
    # text = json.dumps(answ, indent=2, ensure_ascii=False)
    # text2 = text.
    # print(update_massage)
    msg = await send_message(client_session, chat_id=update_massage.chat.id,
                             text=answer,)   # sort_keys=True, ensure_ascii=False),)
    logger.debug(msg.json(indent=2, sort_keys=True))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=settings.port)

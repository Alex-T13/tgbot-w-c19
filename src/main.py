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
from db import crud
from db.crud import create_user
from dirs import DIR_TEMPLATES
from telegram.methods import get_webhook_info
from telegram.methods import send_message
from telegram.methods import set_webhook
from telegram.types import Update
from telegram.types import User
from telegram.types import Message
# from telegram.types import UserListApiSchema
from urls import hide_webhook_token
from urls import PATH_DOCS
from urls import PATH_ROOT
from urls import PATH_SETUP_WEBHOOK
from urls import PATH_WEBHOOK_SECRET
from urls import URL_WEBHOOK
from urls import URL_WEBHOOK_SECRET
from utils import main_switch_update
from utils import get_last_msg

app = FastAPI(
    description="Telegram Bot",
    docs_url=f"{PATH_DOCS}/",
    openapi_url=f"{PATH_DOCS}/openapi.json",
    redoc_url=f"{PATH_DOCS}/redoc/",
    title="Telegram Bot API",
    version="2.2.0",
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
        "path_get_users": f"{PATH_ROOT}/get_users/",
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

    return RedirectResponse(f"{PATH_ROOT}/", status_code=status.HTTP_303_SEE_OTHER, )


@app.post(f"{PATH_WEBHOOK_SECRET}/")
async def handle_webhook(update: Update, client_session: ClientSession = Depends(http_client_session),):
    update_massage = update.message if update.message is not None else update.edited_message

    get_user = crud.get_single_user(update_massage.from_.id)
    logger.debug(f"get single user: {get_user}")
    if get_user:
        if await get_last_msg(update_massage):
            msg_ = await send_message(
                client_session,
                chat_id=update_massage.chat.id,
                text=f"С возвращением {update_massage.from_.first_name}!"
            )
            logger.debug(msg_.json(indent=2, sort_keys=True))
    else:
        user = crud.create_user(update_massage)
        logger.debug(f"created user: {user}")

    save_msg = crud.save_message(update_massage)
    logger.debug(f"save message: {save_msg}")

    answer = await main_switch_update(update_massage, client_session)
    msg = await send_message(client_session, chat_id=update_massage.chat.id, text=answer)
    logger.debug(msg.json(indent=2, sort_keys=True))


@app.post(f"{PATH_ROOT}/get_users/", response_class=HTMLResponse)
async def get_users(request: Request, password: str = Form(...), ):
    if password != settings.admin_password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid password",
        )

    objects = crud.get_all_users()
    logger.debug(f"get users: {objects}")
    users = [
        User(
            id=user.id,
            first_name=user.first_name,
            is_bot=user.is_bot,
            last_name=user.last_name,
            username=user.username,
        )
        for user in objects
    ]

    logger.debug("built users")
    context = {
        "users": users,
        "path_root": f"{PATH_ROOT}/",
    }
    logger.debug("built context")

    response = templates.TemplateResponse("get_users.html", {"request": request, **context})
    return response


# @app.get(f"{PATH_ROOT}/api/test/get-users/", response_class=HTMLResponse)
# async def all_users():
#     objects = get_all_users()
#     logger.debug(f"get single user: {objects}")
#     users = [
#         User(
#             id=user.id,
#             first_name=user.first_name,
#             is_bot=user.is_bot,
#             last_name=user.last_name,
#             username=user.username,
#         )
#         for user in objects
#     ]
#     logger.debug("built users")
#
#     response = UserListApiSchema(data=users).json()
#     logger.debug("build response")
#
#     return response
#
#
@app.post("/api_test/create_user/")
async def create_u(user: Message, ):
    user = create_user(user)
    logger.debug(f"created user: {user}")
    return user


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=settings.port)

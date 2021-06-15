from aiohttp import ClientSession
from fastapi import Depends, FastAPI, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from config import settings
from custom_logging import logger
from db import crud
from dirs import DIR_TEMPLATES
from telegram.methods import get_webhook_info, send_message, set_webhook
from telegram.types import Update, User, Message
from urls import hide_webhook_token, PATH_DOCS, PATH_ROOT, PATH_SETUP_WEBHOOK
from urls import PATH_WEBHOOK_SECRET, URL_WEBHOOK, URL_WEBHOOK_SECRET
from handler_bot_cmd import choice_of_answer
from utils import welcome_back, FuncParameters, language_info


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

    webhook_set = await set_webhook(client_session, webhook_url=f"{URL_WEBHOOK_SECRET}/", )
    if not webhook_set:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="webhook was not set",
        )

    return RedirectResponse(f"{PATH_ROOT}/", status_code=status.HTTP_303_SEE_OTHER, )


@app.post(f"{PATH_WEBHOOK_SECRET}/")
async def handle_webhook(update: Update, client_session: ClientSession = Depends(http_client_session), ):
    update_message = update.message if update.message is not None else update.edited_message

    user = crud.get_user_by_id(update_message.from_.id)
    if not user:
        await send_message(client_session, chat_id=update_message.chat.id, text=language_info())
        user = crud.create_user(update_message)

    args = FuncParameters(
        session=client_session,
        message=update_message,
        localization=user.lang,
    )

    msg_welcome_back = await welcome_back(args)
    if msg_welcome_back:
        await send_message(client_session, chat_id=update_message.chat.id, text=msg_welcome_back)

    crud.save_message(update_message)
    answer = await choice_of_answer(args)
    msg = await send_message(client_session, chat_id=update_message.chat.id, text=answer)
    logger.debug(msg.json(indent=2, sort_keys=True))


@app.post(f"{PATH_ROOT}/get_users/", response_class=HTMLResponse)
async def get_users(request: Request, password: str = Form(...), ):
    if password != settings.admin_password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid password",
        )

    objects = crud.get_all_users()  # !!!!!!!!!objects -> users
    logger.debug(f"get users: {objects}")
    users = [
        User(
            id=user.id,
            first_name=user.first_name,
            is_bot=user.is_bot,
            last_name=user.last_name,
            username=user.username,
        )
        for user in objects  # List!!
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
    user = crud.create_user(user)
    logger.debug(f"created user: {user}")
    return user


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=settings.port)

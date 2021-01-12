import os
import requests
from fastapi import FastAPI
from fastapi import status

PORT = int(os.getenv("PORT", 8000))

HOST = os.getenv("HOST")
assert HOST, "host not set"

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
assert TELEGRAM_TOKEN, "no tg token"

TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

API_URL = "/api/v1"

app = FastAPI(
    description="example of tg bot",
    docs_url=f"{API_URL}/docs/",
    openapi_url=f"{API_URL}/openapi.json",
    redoc_url=f"{API_URL}/redoc/",
    title="XXX API",
    version="1.0.0",
)


@app.post(f"{API_URL}/tg/setup/")
async def tg_setup():
    try:
        payload = {
            "url": f"https://{HOST}/api/v1/tg/",
        }

        resp = requests.post(
            f"{TELEGRAM_API}/setWebhook",
            json=payload,
        )
        print(resp.content)
    except Exception:
        pass


@app.post(f"{API_URL}/tg/")
async def tg(update: Update):
    try:
        payload = {
            "chat_id": update.message.chat.id,
            "text": "ok",
        }

        resp = requests.post(f"{TELEGRAM_API}/sendMessage", json=payload)
        print(resp.content)
    except Exception:
        pass


if __name__ == "__main__" and settings.MODE_DEBUG:
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=PORT)


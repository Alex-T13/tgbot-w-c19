from config import settings

PATH_ROOT = ""

PATH_DOCS = f"{PATH_ROOT}/help"

PATH_SETUP_WEBHOOK = f"{PATH_ROOT}/setup-webhook"

PATH_WEBHOOK = f"{PATH_ROOT}/webhook"
URL_WEBHOOK = f"https://{settings.host}{PATH_WEBHOOK}"

PATH_WEBHOOK_SECRET = f"{PATH_WEBHOOK}/{settings.telegram_webhook_token}"
URL_WEBHOOK_SECRET = f"https://{settings.host}{PATH_WEBHOOK_SECRET}"

URL_TELEGRAM_API = f"https://api.telegram.org/bot{settings.telegram_bot_token}"


def hide_webhook_token(webhook_url: str) -> str:
    try:
        public_path_begin = webhook_url.index(f"{PATH_WEBHOOK}")
        public_path_end = public_path_begin + len(PATH_WEBHOOK)
        public_url = webhook_url[:public_path_end]
        return f"{public_url}/<TOKEN>/"  # :)
    except ValueError:
        return webhook_url

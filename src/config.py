from pydantic import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    admin_password: str = Field(..., env="ADMIN_PASSWORD")
    debug: bool = Field(env="DEBUG", default=False)
    host: str = Field(..., env="HOST")
    port: int = Field(env="PORT", default=8000)
    telegram_bot_token: str = Field(..., env="TELEGRAM_BOT_TOKEN")
    telegram_webhook_token: str = Field(..., env="TELEGRAM_WEBHOOK_TOKEN")

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"
        fields = {
            "from_": "from",
        }


settings = Settings()

if __name__ == "__main__":
    print(settings.json(indent=2, sort_keys=True))

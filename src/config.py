from pydantic import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    admin_password: str = Field(..., env="ADMIN_PASSWORD")
    debug: bool = Field(env="DEBUG", default=False)
    host: str = Field(..., env="HOST")
    port: int = Field(env="PORT", default=8000)
    telegram_bot_token: str = Field(..., env="TELEGRAM_BOT_TOKEN")
    telegram_webhook_token: str = Field(..., env="TELEGRAM_WEBHOOK_TOKEN")
    x_rapidapi_key: str = Field(..., env="X_RAPIDAPI_KEY")
    open_weather_appid: str = Field(..., env="OPEN_WEATHER_APPID")
    database_url: str = Field(..., env="DATABASE_URL")

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

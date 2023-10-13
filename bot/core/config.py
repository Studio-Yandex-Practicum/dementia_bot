from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Main settings."""
    telegram_api_token: str
    webhook_mode: bool
    WEB_SERVER_HOST: str = "127.0.0.1"
    WEB_SERVER_PORT: int = 8080
    # Path to webhook route, on which Telegram will send requests
    WEBHOOK_PATH: str = "/webhook"
    # Secret key to validate requests from Telegram (optional)
    WEBHOOK_SECRET: str = "my-secret"
    # Base URL for webhook will be used to generate webhook URL for Telegram,
    # in this example it is used public DNS with HTTPS support
    BASE_WEBHOOK_URL: str = "https://aiogram.dev/"
    HOST: str = "http://web:8000/"

    class Config:
        env_file = '.env'
        extra = 'ignore'


settings = Settings()

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Main settings."""
    telegram_api_token: str
    webhook_mode: bool

    class Config:
        env_file = '.env'


settings = Settings()

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    google_client_id: str
    google_client_secret: str
    google_refresh_token: str
    database_url: str
    classifier_model: str = "anthropic:claude-haiku-5-5"
    agent_model: str = "anthropic:claude-sonnet-5-5"
    poll_interval_seconds: int = 60
    dashboard_username: str = "admin"
    dashboard_password: str = ""


settings = Settings()

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
import os

load_dotenv()


class Settings(BaseSettings):
    google_client_id: str
    google_client_secret: str
    google_refresh_token: str
    database_url: str
    classifier_model: str = "openai-chat:gpt-oss-120b"
    agent_model: str = "openai-chat:gpt-oss-120b"
    poll_interval_seconds: int = 60
    dashboard_username: str = "admin"
    dashboard_password: str = "Sauravsingh45"


settings = Settings()

# CategoryInfo          : ObjectNotFound: (scoop:String) [Get-Command], CommandNotFoundException
# FullyQualifiedErrorId : CommandNotFoundException,Microsoft.PowerShell.Commands.GetCommandCommand

import json
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import AnyUrl

class Settings(BaseSettings):
    database_url: str = "sqlite:///./taskflow.db"
    jwt_secret: str = "super_secret_key_123"
    jwt_algorithm: str = "HS256"
    email_sender: str = "noreply@taskflow.com"
    sendgrid_api_key: str = "your_sendgrid_key_here"
    
    class Config:
        env_file = ".env"
        # Load from config.json if exists
        @classmethod
        def customise_sources(cls, init_settings, env_settings, file_secret_settings):
            config_path = Path("config.json")
            if config_path.exists():
                with open(config_path) as f:
                    config_data = json.load(f)
                return init_settings, env_settings, lambda: config_data, file_secret_settings
            return init_settings, env_settings, file_secret_settings

settings = Settings()

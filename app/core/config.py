import json
from pathlib import Path
from pydantic import BaseSettings, AnyUrl

class Settings(BaseSettings):
    # ...existing settings...
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
                return init_settings, env_settings, lambda: config_data
            return init_settings, env_settings

settings = Settings()

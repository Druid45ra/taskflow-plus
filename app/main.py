import json
from pydantic import BaseSettings

class Settings(BaseSettings):
    jwt_secret: str
    oauth_providers: dict

    class Config:
        with open("config.json") as f:
            config_data = json.load(f)
        env_file = ".env"
        secrets_dir = "/run/secrets"

settings = Settings()

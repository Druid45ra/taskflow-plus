import json
from pathlib import Path
from pydantic import BaseSettings, AnyUrl

class Settings(BaseSettings):
    # Citeste din .env sau config.json
    database_url: AnyUrl = "sqlite:///./taskflow.db"
    jwt_secret: str = "secret_key_123"
    jwt_algorithm: str = "HS256"
    oauth_providers: dict = {}
    
    class Config:
        env_file = ".env"
        # Încarcă și din config.json dacă există
        @classmethod
        def customise_sources(cls, init_settings, env_settings, file_secret_settings):
            config_path = Path("config.json")
            if config_path.exists():
                with open(config_path) as f:
                    config_data = json.load(f)
                return init_settings, env_settings, lambda: config_data
            return init_settings, env_settings

settings = Settings()

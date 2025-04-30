import os

from google.cloud import secretmanager
from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    # Redis settings
    REDIS_HOST: str = os.getenv("REDIS_HOST")
    REDIS_PORT: int = os.getenv("REDIS_PORT")
    REDIS_USERNAME: str = os.getenv("REDIS_USERNAME")
    REDIS_PASSWORD: str = ""

    @property
    def REDIS_URL(self):
        return (
            f"redis://{self.REDIS_USERNAME}:{self.REDIS_PASSWORD}"
            f"@{self.REDIS_HOST}:{self.REDIS_PORT}"
        )

    # DB settings
    DB_HOST: str = os.getenv("DB_HOST")
    DB_USER: str = os.getenv("DB_USER")
    DB_NAME: str = os.getenv("DB_NAME")
    DB_PASSWORD: str = ""

    @property
    def DB_URL(self):
        return (
            f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}/{self.DB_NAME}"
        )

    SCRAPER_SERVICE_URL: str = os.getenv("SCRAPER_SERVICE_URL")
    ML_INFERENCE_SERVICE_URL: str = os.getenv("ML_INFERENCE_SERVICE_URL")
    SCHEDULER_AUDIENCE: str = os.getenv("SCHEDULER_AUDIENCE")
    SERVICE_ACCOUNT: str = os.getenv("SERVICE_ACCOUNT")
    PROJECT_ID: str = os.getenv("PROJECT_ID")

    JWT_ACCESS_SECRET = ""
    JWT_REFRESH_SECRET = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def get_settings():
    s = Settings()
    client = secretmanager.SecretManagerServiceClient()

    def get_secret(name: str, version: str) -> str:
        secret_name = f"projects/{s.PROJECT_ID}/secrets/{name}/versions/{version}"
        return client.access_secret_version(name=secret_name).payload.data.decode("UTF-8")

    s.REDIS_PASSWORD = get_secret("REDIS_PASSWORD", "1")
    s.DB_PASSWORD = get_secret("DB_PASSWORD", "1")
    s.JWT_ACCESS_SECRET = get_secret("JWT_ACCESS_SECRET", "1")
    s.JWT_REFRESH_SECRET = get_secret("JWT_REFRESH_SECRET", "1")

    return s


settings = get_settings()

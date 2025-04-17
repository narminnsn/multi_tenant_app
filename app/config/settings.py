from pydantic_settings import BaseSettings
from tortoise import Tortoise
from typing import ClassVar
from pydantic import Extra

# TORTOISE_ORM = {
#     "connections": {
#         "default": "postgres://multi_tenant:zQhGyUUkeNov9SQ@localhost/multi_tenant",
#     },
#     "apps": {
#         "models": {
#             "models": ['app.core.models', 'app.tenants.models', "aerich.models"],
#             "default_connection": "default",
#         },
#     },
# }


class Settings(BaseSettings):
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int

    @property
    def DATABASE_URL(self) -> str:
        return (f"postgres://"
                f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}")

    class Config:
        env_file = "./.env"
        env_file_encoding = "utf-8"


settings = Settings()

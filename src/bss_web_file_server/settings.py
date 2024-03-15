from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    server_base_path: str = "./assets/"


settings = Settings()

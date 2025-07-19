from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv


load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    DB_NAME: str
    DB_PASS: str
    DB_USER: str
    DB_PORT: int
    DB_HOST: str

    DB_ECHO: bool
    SECRET_KEY: str
    HOST: list[str]

    access_token_expire_min: int = 36000
    algorithm: str = "HS256"

    @property
    def db_connect(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()

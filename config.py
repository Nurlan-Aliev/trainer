from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
from starlette.templating import Jinja2Templates

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    DB_NAME: str
    DB_PASS: str
    DB_USER: str
    DB_PORT: int
    DB_HOST: str

    SECRET_KEY: str
    DEBUG: bool
    access_token_expire_min: int = 36000
    algorithm: str = "HS256"

    templates: Jinja2Templates = Jinja2Templates(directory="templates")

    @property
    def db_connect(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()

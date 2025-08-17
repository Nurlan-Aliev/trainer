from pydantic import BaseModel


class BaseWord(BaseModel):
    word_en: str
    word_ru: str | None = None
    word_az: str | None = None


class WordSchemas(BaseWord):
    id: int

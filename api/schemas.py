from pydantic import BaseModel


class BaseWord(BaseModel):
    word: str
    translate_ru: str | None = None
    translate_az: str | None = None


class WordSchemas(BaseWord):
    id: int

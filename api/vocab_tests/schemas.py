from pydantic import BaseModel


class TestSchema(BaseModel):
    answer: str
    id: int


class ConstructorSchema(BaseModel):
    id: int
    word: str
    word_ru: str | None = None
    word_az: str | None = None


class TranslateSchemas(BaseModel):
    word_id: int
    word_ru: str
    options: list[str]

from pydantic import BaseModel


class TestSchema(BaseModel):
    user_answer: str
    word_id: int


class ConstructorSchema(BaseModel):
    word_id: int
    word_ru: str | None = None
    word_az: str | None = None


class TranslateSchemas(BaseModel):
    word_id: int
    question: str
    options: list[str]

from pydantic import BaseModel


class TestSchema(BaseModel):
    answer: str
    id: int


class ConstructorSchema(BaseModel):
    id: int
    word: str
    translate_ru: str | None = None
    translate_az: str | None = None

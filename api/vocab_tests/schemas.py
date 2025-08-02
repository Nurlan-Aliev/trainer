from pydantic import BaseModel


class TestSchema(BaseModel):
    answer: str
    id: int
    translate_ru: str | None = None

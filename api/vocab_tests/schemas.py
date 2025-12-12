from pydantic import BaseModel
from api.vocab_tests.custom_enum import Language


class BaseTestSchema(BaseModel):
    word_id: int


class TestSchema(BaseTestSchema):
    user_answer: str
    language: Language


class ConstructorSchema(BaseTestSchema):
    word_ru: str | None = None
    word_az: str | None = None
    word_en: str | None = None


class TranslateSchemas(BaseTestSchema):
    question: dict
    options: list[dict]


class Remember(BaseTestSchema):
    remember: bool

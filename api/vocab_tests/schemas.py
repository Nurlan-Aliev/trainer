from pydantic import BaseModel


class BaseTestSchema(BaseModel):
    word_id: int


class TestSchema(BaseTestSchema):
    user_answer: str


class ConstructorSchema(BaseTestSchema):
    word_ru: str | None = None
    word_az: str | None = None
    word_en: str | None = None


class TranslateSchemas(BaseTestSchema):
    question: str
    options: list[str]


class ForgotRemember(BaseTestSchema):
    remember: bool

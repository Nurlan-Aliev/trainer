from pydantic import BaseModel


class WordSchemas(BaseModel):
    id: int
    word: str

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Word(Base):
    word: Mapped[str] = mapped_column(primary_key=True)
    translate_ru: Mapped[str] = mapped_column(nullable=True)
    translate_az: Mapped[str] = mapped_column(nullable=True)


class LearnedWord(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    word_id: Mapped[int] = mapped_column(ForeignKey("words.id"))

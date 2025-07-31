from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class Word(Base):
    word: Mapped[str]
    translate_ru: Mapped[str] = mapped_column(nullable=True)
    translate_az: Mapped[str] = mapped_column(nullable=True)


class LearnedWord(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    word_id: Mapped[int] = mapped_column(ForeignKey("words.id"))
    __table_args__ = (UniqueConstraint("user_id", "word_id"),)

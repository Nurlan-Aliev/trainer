from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class Word(Base):
    word_en: Mapped[str]
    word_ru: Mapped[str] = mapped_column(nullable=True)
    word_az: Mapped[str] = mapped_column(nullable=True)
    word_to_learn = relationship("WordsToLearn", back_populates="word")
    learned = relationship("LearnedWord", back_populates="learned_word")


class LearnedWord(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    word_id: Mapped[int] = mapped_column(ForeignKey("words.id"))
    learned_word = relationship("Word", back_populates="learned")
    __table_args__ = (UniqueConstraint("user_id", "word_id"),)


class WordsToLearn(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    word_id: Mapped[int] = mapped_column(ForeignKey("words.id"))
    word = relationship("Word", back_populates="word_to_learn")

    __table_args__ = (UniqueConstraint("user_id", "word_id"),)

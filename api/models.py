from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class WordsList(Base):
    word: Mapped[str]
    translate_ru: Mapped[str] = mapped_column(nullable=True)
    translate_az: Mapped[str] = mapped_column(nullable=True)

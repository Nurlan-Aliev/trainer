from sqlalchemy import ForeignKey, UniqueConstraint, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from api.vocab_tests.word_test_enum import Test
from database import Base


class UserWordTestResult(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    word_id: Mapped[int] = mapped_column(ForeignKey("words.id"))
    test: Mapped[Test] = mapped_column(SQLEnum(Test, name="test_enum"), nullable=False)

    __table_args__ = (UniqueConstraint("user_id", "word_id", "test"),)

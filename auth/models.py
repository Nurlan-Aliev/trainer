from sqlalchemy import String, LargeBinary, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class User(Base):
    name: Mapped[str] = mapped_column(String(30))
    surname: Mapped[str] = mapped_column(String(30))
    password: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    status: Mapped[str] = mapped_column(String(10), default="user")
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    is_active: Mapped[bool] = mapped_column(server_default=text("false"), default=True)

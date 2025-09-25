from sqlalchemy import String, LargeBinary, text, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from auth.role_enum import Role

from database import Base


class User(Base):
    name: Mapped[str] = mapped_column(String(30))
    surname: Mapped[str] = mapped_column(String(30), nullable=True)
    password: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    role: Mapped[Role] = mapped_column(
        SQLEnum(Role, name="role_enum"), nullable=False, default=Role.user.value
    )

    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    is_active: Mapped[bool] = mapped_column(server_default=text("false"), default=True)

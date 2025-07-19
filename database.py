from asyncio import current_task
from datetime import datetime, timezone
from sqlalchemy import DateTime
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
    AsyncSession,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
from config import settings


class Base(DeclarativeBase):
    @declared_attr.directive
    def __tablename__(cls):
        return f"{cls.__name__.lower()}s"

    id: Mapped[int] = mapped_column(primary_key=True)

    create_at: Mapped[DateTime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc).replace(microsecond=0, tzinfo=None),
        nullable=False,
    )


class DataBaseHelper:
    def __init__(self, url: str, echo=False):
        self.async_engine = create_async_engine(
            url=url,
            echo=echo,
        )
        self.session_factory = async_sessionmaker(
            self.async_engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def get_scope_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session

    async def session_dependency(self) -> AsyncSession:
        async with self.session_factory() as session:
            yield session


db_helper = DataBaseHelper(
    settings.db_connect,
)

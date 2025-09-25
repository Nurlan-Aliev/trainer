from fastapi import HTTPException, status
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from auth.models import User
from config import settings


async def create_user(
    name: str,
    login: EmailStr,
    hash_pass: bytes,
    session: AsyncSession,
):
    user = await get_user_by_email(login, session)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="user already exist",
        )
    new_user = User(name=name, email=login, password=hash_pass)
    session.add(new_user)
    await session.commit()


async def get_user_by_email(email, session):
    stmt = select(User).where(User.email == email)
    result = await session.scalars(stmt)
    return result.first()


async def get_user_by_id(idx, session):
    stmt = select(User).where(User.id == idx)
    result = await session.scalars(stmt)
    return result.first()


def get_black_list():
    black_refresh_list = settings.redis_db.lrange("black_refresh_list", 0, -1)
    return black_refresh_list


def add_in_black_list(token):
    settings.redis_db.rpush("black_refresh_list", token)

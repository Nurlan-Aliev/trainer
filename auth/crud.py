from fastapi import Depends, HTTPException, status, Form
from auth.db_user import get_user
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from database import db_helper
from auth.models import User
from auth.validator import hash_password, auth_user


async def create_user(
    name: str = Form(),
    surname: str = Form(),
    login: EmailStr = Form(),
    password: str = Form(),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    hash_pass = hash_password(password)
    user = await get_user(login, session)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="user already exist",
        )
    new_user = User(name=name, surname=surname, email=login, password=hash_pass)
    session.add(new_user)
    await session.commit()
    return await auth_user(login, password, session)

from fastapi import Depends, HTTPException, status, Form
from auth.db_user import get_user
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from database import db_helper
from auth.models import User
from auth import validator


async def create_user(
    name: str = Form(),
    login: EmailStr = Form(),
    password: str = Form(),
    re_password: str = Form(),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    if re_password != password:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Passwords do not match",
        )

    hash_pass = validator.hash_password(password)
    user = await get_user(login, session)

    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="user already exist",
        )
    new_user = User(name=name, email=login, password=hash_pass)
    session.add(new_user)
    await session.commit()
    return await validator.auth_user(login, password, session)

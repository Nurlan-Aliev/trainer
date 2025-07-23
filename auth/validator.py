import jwt
from fastapi import Depends, HTTPException, status, Form
from auth.jwt_helper import decode_jwt
from auth.schemas import UserAuthSchema
from auth.db_user import get_user
from pydantic import EmailStr
from fastapi.security import HTTPBearer
import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession
from database import db_helper


http_bearer = HTTPBearer(auto_error=False)


def get_current_token_payload(
    token: HTTPBearer = Depends(http_bearer),
) -> dict:
    """returns payload from jwt"""
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    try:
        payload = decode_jwt(token=token.credentials)
        return payload
    except jwt.exceptions.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"invalid token error"
        )


async def get_user_by_token_sub(
    payload: dict, session: AsyncSession = Depends(db_helper.session_dependency)
) -> UserAuthSchema:
    """
    Returns the user by his sub
    """
    email: str | None = payload.get("email")
    if user := await get_user(email, session):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="user not found",
    )


def is_admin(payload: dict = Depends(get_current_token_payload)):
    if is_active(payload) and payload.get("status") == "admin":
        return payload
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="You don’t have permission"
    )


def is_active(payload: dict = Depends(get_current_token_payload)):
    if payload.get("is_active"):
        return payload
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="user is not active"
    )


async def validate_auth_user(
    login: EmailStr = Form(),
    password: str = Form(),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await auth_user(login, password, session)


async def auth_user(
    login,
    password,
    session,
):
    unauthed_exp = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password"
    )
    if not (user := await get_user(login, session)):
        raise unauthed_exp
    if not validate_password(password=password, hashed_password=user.password):
        raise unauthed_exp
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not active"
        )
    return user


def validate_password(
    password: str,
    hashed_password: bytes,
) -> bool:
    return bcrypt.checkpw(password=password.encode(), hashed_password=hashed_password)


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)

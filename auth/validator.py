import jwt
from auth.jwt_helper import decode_jwt
from auth.schemas import UserAuthSchema
from auth.db_user import get_user
from fastapi.security import HTTPBearer
import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession
from database import db_helper
from fastapi import HTTPException, status, Depends, Request


UNAUTHORIZED = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="You need to log in"
)
http_bearer = HTTPBearer(auto_error=False)


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


async def auth_user(
    login,
    password,
    session,
):

    if not (user := await get_user(login, session)):
        return None
    if not validate_password(password=password, hashed_password=user.password):
        return None
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


def get_current_token_payload(
    token: str | bytes,
) -> dict:
    try:
        payload = decode_jwt(token=token)
        return payload
    except jwt.exceptions.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"invalid token error"
        )
    except AttributeError:
        raise UNAUTHORIZED


def is_current_token(
    request: Request,
) -> dict | None:
    token = request.cookies.get("access_token")
    if not token:
        raise UNAUTHORIZED
    return get_current_token_payload(token)


def is_user_logged_in(
    request: Request,
) -> dict | None:
    token = request.cookies.get("access_token")
    if not token:
        return None
    return get_current_token_payload(token)

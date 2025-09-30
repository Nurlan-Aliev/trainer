import jwt
from pydantic import EmailStr
from auth.jwt_helper import decode_jwt
from auth.schemas import UserAuthSchema
from auth import crud
from fastapi.security import HTTPBearer
import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status, Depends, Request


UNAUTHORIZED = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="You need to log in"
)
http_bearer = HTTPBearer(auto_error=False)


async def get_user_by_token_sub(payload: dict, session: AsyncSession) -> UserAuthSchema:
    """
    Returns the user by his sub
    """
    idx: int | None = payload.get("id")
    if user := await crud.get_user_by_id(idx, session):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="user not found",
    )


async def auth_user(
    login: EmailStr,
    password: str,
    session: AsyncSession,
):
    if not (user := await crud.get_user_by_email(login, session)):
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


def get_current_token_payload(token: str | bytes, token_type: str) -> dict:
    invalid_token = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail=f"invalid token error"
    )
    try:
        payload = decode_jwt(token=token)

        if not payload.get("token_type") == token_type:
            raise invalid_token

        return payload

    except jwt.exceptions.InvalidTokenError as e:
        raise invalid_token
    except AttributeError:
        raise UNAUTHORIZED


def is_current_access_token(token: HTTPBearer = Depends(http_bearer)) -> dict | None:
    if not token:
        raise UNAUTHORIZED
    return get_current_token_payload(token.credentials, "access")


def is_current_refresh_token(request: Request) -> dict | None:
    token = request.cookies.get("refresh_token")
    black_refresh_list = crud.get_black_list()

    if token in black_refresh_list:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"invalid token error"
        )

    if not token:
        raise UNAUTHORIZED
    return get_current_token_payload(token, "refresh")


def is_user_logged_in(
    request: Request,
) -> dict | None:
    token = request.cookies.get("access_token")
    if not token:
        return None
    return get_current_token_payload(token, "access")

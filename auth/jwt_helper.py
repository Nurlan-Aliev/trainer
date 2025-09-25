from datetime import timedelta, datetime, UTC
import jwt
from config import settings
from auth.schemas import UserAuthSchema


def create_access_token(
    user: UserAuthSchema,
) -> str:
    jwt_pyload = {
        "token_type": "access",
        "id": user.id,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active,
    }
    minutes = timedelta(minutes=settings.access_token_expire_min)
    return encode_jwt(payload=jwt_pyload, minutes=minutes)


def create_refresh_token(user: UserAuthSchema) -> str:
    jwt_pyload = {
        "token_type": "refresh",
        "id": user.id,
    }
    minutes = timedelta(minutes=settings.refresh_token_expire_min)
    return encode_jwt(payload=jwt_pyload, minutes=minutes)


def encode_jwt(
    payload: dict,
    minutes: timedelta,
) -> str:
    to_encode = payload.copy()
    utcnow = datetime.now(UTC)
    expire = utcnow + minutes
    to_encode.update(
        exp=expire,
        iat=utcnow,
    )
    encoded = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.algorithm)
    return encoded


def decode_jwt(
    token: str | bytes,
):
    decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.algorithm])
    return decoded

from datetime import timedelta, datetime, UTC
import jwt
from config import settings
from auth.schemas import UserAuthSchema


def create_jwt(
    user: UserAuthSchema,
) -> str:

    jwt_pyload = {
        "id": user.id,
        "email": user.email,
        "status": user.status,
        "is_active": user.is_active,
    }

    return encode_jwt(
        payload=jwt_pyload,
    )


def encode_jwt(
    payload: dict,
):
    to_encode = payload.copy()
    utcnow = datetime.now(UTC)
    expire = utcnow + timedelta(minutes=settings.access_token_expire_min)
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

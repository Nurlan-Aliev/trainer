from pydantic import BaseModel, EmailStr


class UserAuthSchema(BaseModel):
    id: int
    email: EmailStr
    password: bytes
    status: str
    is_active: bool

from pydantic import BaseModel, EmailStr
from auth.role_enum import Role


class UserAuthSchema(BaseModel):
    id: int
    email: EmailStr
    role: Role
    is_active: bool

from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth.schemas import UserAuthSchema
from auth import jwt_helper
from auth.validator import validate_auth_user
from auth.crud import create_user


http_bearer = HTTPBearer(auto_error=False)
router = APIRouter(tags=["login"], dependencies=[Depends(http_bearer)])


@router.post("/sign_in")
async def auth_user_issue_jwt(
    user: UserAuthSchema = Depends(validate_auth_user),
):
    access_token = jwt_helper.create_jwt(user)
    return access_token


@router.post("/sign_up")
async def sign_up(user: UserAuthSchema = Depends(create_user)):
    access_token = jwt_helper.create_jwt(user)
    return access_token


@router.get("/users/me")
def read_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
):
    if not credentials:
        return "error"
    return {"scheme": credentials.scheme, "credentials": credentials.credentials}

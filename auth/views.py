from typing import Annotated
from fastapi import APIRouter, Depends, Response, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth.schemas import UserAuthSchema
from auth import jwt_helper
from auth.utils import sign_in
from auth.validator import validate_auth_user
from auth.crud import create_user
from fastapi.responses import RedirectResponse


http_bearer = HTTPBearer(auto_error=False)
router = APIRouter(dependencies=[Depends(http_bearer)])


@router.post("/sign_in", response_class=RedirectResponse)
def auth_user_issue_jwt(
    request: Request,
    user: UserAuthSchema = Depends(validate_auth_user),
):
    return sign_in(request, user)


@router.post("/sign_up")
async def sign_up(request: Request, user: UserAuthSchema = Depends(create_user)):
    return sign_in(request, user)


@router.get("/users/me")
def read_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
):
    if not credentials:
        return "error"
    return {"scheme": credentials.scheme, "credentials": credentials.credentials}

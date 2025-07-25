from typing import Annotated
from fastapi import APIRouter, Depends, Response, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth.schemas import UserAuthSchema
from auth import jwt_helper
from auth.validator import validate_auth_user
from auth.crud import create_user
from fastapi.responses import RedirectResponse


http_bearer = HTTPBearer(auto_error=False)
router = APIRouter(dependencies=[Depends(http_bearer)])


@router.post("/sign_in", response_class=RedirectResponse)
def auth_user_issue_jwt(
    request: Request,
    response: Response,
    user: UserAuthSchema = Depends(validate_auth_user),
):
    access_token = jwt_helper.create_jwt(user)
    redirect_url = request.url_for("get_home_page")
    response = RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)

    response.set_cookie(
        key="access_token",
        value=access_token,
        secure=True,
        httponly=True,
        max_age=3600,
    )

    return response


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

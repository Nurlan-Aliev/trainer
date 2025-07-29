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
def sign_up(request: Request, user: UserAuthSchema = Depends(create_user)):
    return sign_in(request, user)


@router.get('/sign_out')
def sign_out(request: Request):
    redirect_url = request.url_for("get_home_page")
    response = RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie('access_token')
    return response
from fastapi import (
    APIRouter,
    Depends,
    status,
    Response,
    HTTPException,
    Request,
)
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from auth.crud import add_in_black_list
from auth.utils import sign_in
from auth import validator, jwt_helper
from auth import crud
from fastapi import Form
from pydantic import EmailStr
from auth.validator import is_current_access_token
from database import db_helper


http_bearer = HTTPBearer(auto_error=False)
router = APIRouter(dependencies=[Depends(http_bearer)])


@router.post("/login")
async def auth_user_issue_jwt(
    login: EmailStr = Form(),
    password: str = Form(),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    user = await validator.auth_user(login, password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="incorrect login or password",
        )
    return sign_in(user)


@router.post("/refresh")
async def refresh_token(
    payload: dict = Depends(validator.is_current_refresh_token),
    session: AsyncSession = Depends(db_helper.session_dependency),
):

    user = await validator.get_user_by_token_sub(payload, session)
    return jwt_helper.create_access_token(user)


@router.post("/sign_up")
async def sign_up(
    name: str = Form(),
    login: EmailStr = Form(),
    password: str = Form(),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    hash_pass = validator.hash_password(password)
    await crud.create_user(name, login, hash_pass, session)
    user = await validator.auth_user(login, password, session)
    return sign_in(user)


@router.post("/logout")
def sign_out(request: Request):
    token = request.cookies.get("refresh_token")
    if token:
        add_in_black_list(token)

    response = Response()
    response.delete_cookie("refresh_token")
    return response


@router.get("/me")
def about_me(
    user: dict | None = Depends(is_current_access_token),
):
    return user

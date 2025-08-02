from fastapi import APIRouter, Depends, status, Request
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from auth.schemas import UserAuthSchema
from auth.utils import sign_in
from auth import validator
from auth.crud import create_user
from fastapi import Form
from pydantic import EmailStr
from fastapi.responses import RedirectResponse
from database import db_helper

http_bearer = HTTPBearer(auto_error=False)
router = APIRouter(dependencies=[Depends(http_bearer)])


@router.post("/sign_in", response_class=RedirectResponse)
async def auth_user_issue_jwt(
    request: Request,
    login: EmailStr = Form(),
    password: str = Form(),
    session: AsyncSession = Depends(db_helper.session_dependency),
):

    user = await validator.auth_user(login, password, session)
    if not user:
        redirect_url = request.url_for("sign_in")
        return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
    return sign_in(request, user)


@router.post("/sign_up")
def sign_up(request: Request, user: UserAuthSchema = Depends(create_user)):
    return sign_in(request, user)


@router.get("/sign_out")
def sign_out(request: Request):
    redirect_url = request.url_for("get_home_page")
    response = RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("access_token")
    return response

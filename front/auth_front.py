from fastapi import APIRouter, Request, Depends
from auth.validator import is_user_logged_in
from fastapi.responses import RedirectResponse

from config import settings


router = APIRouter()


@router.get("/sign_up")
def sign_up(
    request: Request,
    user: dict | None = Depends(is_user_logged_in),
):
    if user:
        redirect_url = request.url_for("get_home_page")
        return RedirectResponse(redirect_url)
    return settings.templates.TemplateResponse(
        "auth/sign_up.html",
        {
            "user": user,
            "request": request,
        },
    )


@router.get("/sign_in")
def sign_in(
    request: Request,
    user: dict | None = Depends(is_user_logged_in),
):
    if user:
        redirect_url = request.url_for("get_home_page")
        return RedirectResponse(redirect_url)

    return settings.templates.TemplateResponse(
        "auth/sign_in.html",
        {
            "user": user,
            "request": request,
        },
    )

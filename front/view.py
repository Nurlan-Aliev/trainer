from fastapi import APIRouter, Request, Depends
from starlette.templating import Jinja2Templates
from auth.validator import is_user_logged_in
from fastapi.responses import RedirectResponse

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
def get_home_page(
    request: Request,
    user: dict | None = Depends(is_user_logged_in),
):
    return templates.TemplateResponse(
        "homepage.html",
        {
            "user": user,
            "request": request,
        },
    )


@router.get("/learn")
def learn_word(
    request: Request,
    user: dict | None = Depends(is_user_logged_in),
):
    if not user:
        redirect_url = request.url_for("sign_in")
        return RedirectResponse(redirect_url)
    return templates.TemplateResponse(
        "learn.html",
        {
            "user": user,
            "request": request,
        },
    )


@router.get("/sign_up")
def sign_up(
    request: Request,
    user: dict | None = Depends(is_user_logged_in),
):
    if user:
        redirect_url = request.url_for("get_home_page")
        return RedirectResponse(redirect_url)
    return templates.TemplateResponse(
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

    return templates.TemplateResponse(
        "auth/sign_in.html",
        {
            "user": user,
            "request": request,
        },
    )

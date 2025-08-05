from fastapi import APIRouter, Request, Depends
from auth.validator import is_user_logged_in
from fastapi.responses import RedirectResponse
from config import settings


router = APIRouter()


@router.get("/learn")
def learn_word(
    request: Request,
    user: dict | None = Depends(is_user_logged_in),
):
    if not user:
        redirect_url = request.url_for("sign_in")
        return RedirectResponse(redirect_url)
    return settings.templates.TemplateResponse(
        "learn.html",
        {
            "user": user,
            "request": request,
        },
    )


@router.get("/train_list")
def train_list(
    request: Request,
    user: dict | None = Depends(is_user_logged_in),
):
    if not user:
        redirect_url = request.url_for("sign_in")
        return RedirectResponse(redirect_url)
    return settings.templates.TemplateResponse(
        "vocab_tests/vocab_test_list.html",
        {
            "user": user,
            "request": request,
        },
    )


@router.get("/constructor")
def constructor(
    request: Request,
    user: dict | None = Depends(is_user_logged_in),
):
    if not user:
        redirect_url = request.url_for("sign_in")
        return RedirectResponse(redirect_url)
    return settings.templates.TemplateResponse(
        "vocab_tests/constructor.html",
        {
            "user": user,
            "request": request,
        },
    )


@router.get("/translate")
def translate(
    request: Request,
    user: dict | None = Depends(is_user_logged_in),
):
    pass


@router.get("/rev_translate")
def rev_translate(
    request: Request,
    user: dict | None = Depends(is_user_logged_in),
):
    pass

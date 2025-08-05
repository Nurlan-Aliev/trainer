from fastapi import APIRouter, Request, Depends
from auth.validator import is_user_logged_in


from config import settings


router = APIRouter()


@router.get("/")
def get_home_page(
    request: Request,
    user: dict | None = Depends(is_user_logged_in),
):
    return settings.templates.TemplateResponse(
        "homepage.html",
        {
            "user": user,
            "request": request,
        },
    )

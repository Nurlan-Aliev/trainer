from fastapi import APIRouter, Request
from starlette.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
def get_home_page(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
        },
    )


@router.get("/sign_in")
def sign_up(request: Request):
    return templates.TemplateResponse(
        "sign_in.html",
        {
            "request": request,
        },
    )

from fastapi import APIRouter, Request, Depends
from auth.validator import is_user_logged_in
from config import settings
from api import crud
from sqlalchemy.ext.asyncio import AsyncSession
from database import db_helper


router = APIRouter()


@router.get("/")
async def get_home_page(
    request: Request,
    session: AsyncSession = Depends(db_helper.session_dependency),
    user: dict | None = Depends(is_user_logged_in),
):

   
    word_count = await crud.get_count_word(user, session)  if user else 0
    return settings.templates.TemplateResponse(
        "homepage.html",
        {
            "user": user,
            'word_count':word_count,
            "request": request,
        },
    )

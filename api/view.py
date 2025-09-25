from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api import crud as api_crud
from api import schemas
from auth import crud as auth_crud
from auth.validator import is_current_access_token
from database import db_helper
from api.models import LearnedWord, WordsToLearn


router = APIRouter(tags=["api"])


@router.get("/")
async def get_10_words(
    skip: int = 0,
    user: dict = Depends(is_current_access_token),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """
    Get 10 words to learn
    :return: list of 10 words
    """
    word_list = await api_crud.get_10_words(skip, user.get("email"), session)
    return [
        schemas.WordSchemas(
            id=word.id,
            word_en=word.word_en,
            word_az=word.word_az,
            word_ru=word.word_ru,
        )
        for word in word_list
    ]


@router.post("/learned")
async def learned_word(
    word: schemas.WordSchemas,
    user: dict | None = Depends(is_current_access_token),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """
    get 10 word need to learn
    """
    user = await auth_crud.get_user_by_email(user["email"], session)
    if not await api_crud.get_word_to_learn(word, user, LearnedWord, session):
        await api_crud.insert_word(word, user, LearnedWord, session)


@router.post("/to_learn")
async def to_learn_word(
    word: schemas.WordSchemas,
    user: dict | None = Depends(is_current_access_token),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """
    add word to the list need learn
    """
    user = await auth_crud.get_user_by_email(user["email"], session)
    if not await api_crud.get_word_to_learn(word, user, LearnedWord, session):
        await api_crud.insert_word(word, user, WordsToLearn, session)


@router.get("/learned_word_count")
async def learned_word_count(
    user: dict | None = Depends(is_current_access_token),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await api_crud.get_count_word(user, session)

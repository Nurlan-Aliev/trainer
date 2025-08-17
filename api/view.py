from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api import crud
from api import schemas
from auth.db_user import get_user
from auth.validator import is_current_token
from database import db_helper
from api.models import LearnedWord, WordsToLearn


router = APIRouter(tags=["api"])


@router.get("/")
async def get_10_words(
    skip: int = 0,
    user: dict = Depends(is_current_token),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """
    Get 10 words to learn
    :return: list of 10 words
    """
    word_list = await crud.get_10_words(skip, user.get("email"), session)
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
    user: dict | None = Depends(is_current_token),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """
    get 10 word need to learn
    """
    user = await get_user(user["email"], session)
    if not await crud.get_word_to_learn(word, user, LearnedWord, session):
        await crud.insert_word(word, user, LearnedWord, session)


@router.post("/to_learn")
async def to_learn_word(
    word: schemas.WordSchemas,
    user: dict | None = Depends(is_current_token),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """
    add word to the list need learn
    """
    user = await get_user(user["email"], session)
    if not await crud.get_word_to_learn(word, user, LearnedWord, session):
        await crud.insert_word(word, user, WordsToLearn, session)


@router.post("/add_word")
async def add_word(
    word: schemas.BaseWord,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """
    add a new words in the list
    """
    await crud.add_new_word(word, session)
    return "word added"


@router.patch("/update")
async def update_word(
    update_data: schemas.WordSchemas,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """
    update words
    """
    word = await crud.update_word_db(update_data, session)
    return word

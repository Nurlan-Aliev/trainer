from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api import crud
from api.schemas import WordSchemas, BaseWord
from auth.validator import is_current_token
from database import db_helper


router = APIRouter()


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
    word_list = await crud.get_10_books(skip, user.get("email"), session)
    return [
        WordSchemas(
            id=word.id,
            word=word.word,
            translate_az=word.translate_az,
            translate_ru=word.translate_ru,
        )
        for word in word_list
    ]


@router.post("/learned")
async def learned_word(
    word: WordSchemas,
    user: dict | None = Depends(is_current_token),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """
    add param word to the learned list
    :return: count of learned word
    """
    await crud.get_word_learned(word, user["email"], session)


@router.post("/add_word")
async def add_word(
    word: BaseWord,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """
    add a new words in the list
    """
    await crud.add_new_word(word, session)
    return "word added"


@router.patch("/update")
async def update_word(
    update_data: WordSchemas,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """
    update words
    """
    word = await crud.update_word_db(update_data, session)
    return word

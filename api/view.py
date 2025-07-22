from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.crud import get_10_books, get_word_learned, get_count_learned_word
from api.schemas import WordSchemas
from auth.validator import get_current_token_payload
from database import db_helper


router = APIRouter()


@router.get("/")
async def get_10_words(session: AsyncSession = Depends(db_helper.session_dependency)):
    """
    Get 10 words to learn
    :return: list of 10 words
    """
    return await get_10_books(session)


@router.post("/learned")
async def learned_word(
    word: WordSchemas,
    user: dict | None = Depends(get_current_token_payload),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """
    add param word to the learned list
    :return: count of learned word
    """
    await get_word_learned(word, user["email"], session)
    count = await get_count_learned_word(user["email"], session)
    return count

from typing import Sequence
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from api.models import LearnedWord
from sqlalchemy.orm import joinedload, selectinload


async def get_10_learned_word(
    user: dict, session: AsyncSession
) -> Sequence[LearnedWord]:
    """
    get 10 random words which is not learned
    """
    stmt = (
        select(LearnedWord)
        .options(selectinload(LearnedWord.learned_word))
        .where(LearnedWord.user_id == user["id"])
        .order_by(func.random())
        .limit(10)
    )
    result = await session.scalars(stmt)
    words = result.all()
    return words


async def delete_from_learned_list(word_id: int, user: dict, session: AsyncSession):
    stmt = (
        select(LearnedWord)
        .where(LearnedWord.word_id == word_id)
        .where(LearnedWord.user_id == user["id"])
    )
    word_obj = await session.scalar(stmt)

    if word_obj:
        await session.delete(word_obj)
        await session.commit()


async def get_word(
    word_idx: int,
    user_idx: int,
    session: AsyncSession,
):

    stmt = (
        select(LearnedWord)
        .where(LearnedWord.word_id == word_idx)
        .where(LearnedWord.user_id == user_idx)
        .options(joinedload(LearnedWord.learned_word))
    )
    word = await session.scalar(stmt)
    return word


from typing import Sequence
from sqlalchemy import select, exists, and_
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import Word, LearnedWord, WordsToLearn
from api import schemas
from auth.crud import get_user
from typing import Type

from auth.models import User


async def get_10_words(
    skip: int, user_email: str, session: AsyncSession
) -> Sequence[Word]:
    """
    get 10 random words which is not learned
    """
    user = await get_user(user_email, session)

    subquery_learned = select(1).where(
        and_(
            LearnedWord.word_id == Word.id,
            LearnedWord.user_id == user.id,
        )
    )

    subquery_to_learn = select(1).where(
        and_(
            WordsToLearn.word_id == Word.id,
            WordsToLearn.user_id == user.id,
        )
    )
    stmt = (
        select(Word)
        .where(~exists(subquery_learned))
        .where(~exists(subquery_to_learn))
        .order_by(Word.id)
        .offset(skip)
        .limit(10)
    )
    result = await session.scalars(stmt)
    words = result.all()
    return words


async def get_word_to_learn(
    word: schemas.WordSchemas,
    user: User,
    table: Type[LearnedWord] | Type[WordsToLearn],
    session: AsyncSession,
):

    stmt = select(table).where(table.word_id == word.id).where(table.user_id == user.id)
    return await session.scalar(stmt)


async def insert_word(
    word: schemas.WordSchemas,
    user: User,
    table: Type[LearnedWord] | Type[WordsToLearn],
    session: AsyncSession,
) -> None:
    """
    add word to learned table
    """
    added_word = table(
        user_id=user.id,
        word_id=word.id,
    )
    session.add(added_word)
    await session.commit()

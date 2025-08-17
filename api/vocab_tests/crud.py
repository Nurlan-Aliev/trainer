from typing import Sequence
from sqlalchemy import select, func, and_, exists, delete
from sqlalchemy.ext.asyncio import AsyncSession
from api.models import Word, LearnedWord, WordsToLearn
from api.vocab_tests.models import UserWordTestResult
from sqlalchemy.orm import joinedload, selectinload

from api.vocab_tests.my_enum import Test
from auth.db_user import get_user

COUNT_OF_TEST = 3


async def get_word(
    word_idx: int,
    user_idx: int,
    session: AsyncSession,
):
    stmt = (
        select(WordsToLearn)
        .where(WordsToLearn.word_id == word_idx)
        .where(WordsToLearn.user_id == user_idx)
        .options(joinedload(WordsToLearn.word))
    )
    word = await session.scalar(stmt)
    return word


async def add_test_in_db(
    word: Word,
    user: dict,
    test: str,
    session: AsyncSession,
):
    stmt_select = (
        select(UserWordTestResult)
        .where(UserWordTestResult.user_id == user["id"])
        .where(UserWordTestResult.word_id == word.id)
        .where(UserWordTestResult.test == test)
    )

    user_test_word = await session.scalar(stmt_select)
    if user_test_word:
        return "test was already added"

    stmt = UserWordTestResult(user_id=user["id"], word_id=word.id, test=test)
    session.add(stmt)
    await session.flush()
    await is_learned(word, user, session)
    await session.commit()
    return "test was added"


async def is_learned(
    word: Word,
    user: dict,
    session: AsyncSession,
):
    stmt = (
        select(func.count())
        .where(UserWordTestResult.user_id == user["id"])
        .where(UserWordTestResult.word_id == word.id)
    )
    test_count = (await session.execute(stmt)).scalar_one()
    if test_count == COUNT_OF_TEST:
        stmt = LearnedWord(user_id=user["id"], word_id=word.id)
        session.add(stmt)
        await clean_data(WordsToLearn, word, user, session)
        await clean_data(UserWordTestResult, word, user, session)


async def get_10_word_for_learn(
    user: dict, test: Test, session: AsyncSession
) -> Sequence[WordsToLearn]:
    """
    get 10 random words which is not learned
    """
    subquery = select(1).where(
        and_(
            UserWordTestResult.word_id == WordsToLearn.word_id,
            UserWordTestResult.user_id == WordsToLearn.user_id,
            UserWordTestResult.test == test,
        )
    )
    stmt = (
        select(WordsToLearn)
        .options(selectinload(WordsToLearn.word))
        .where(~exists(subquery))
        .where(WordsToLearn.user_id == user["id"])
        .order_by(func.random())
        .limit(10)
    )
    result = await session.scalars(stmt)
    words = result.all()
    return words


async def get_random_words(limit: int, session: AsyncSession):
    stmt = select(Word).limit(limit * 4)
    words_list = await session.scalars(stmt)
    return words_list.all()


async def clean_data(model, word: Word, user: dict, session: AsyncSession):
    stmt = (
        delete(model).where(model.user_id == user["id"]).where(model.word_id == word.id)
    )
    await session.execute(stmt)

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from api.models import Word, LearnedWord, WordsToLearn
from api.schemas import WordSchemas
from api.vocab_tests.models import UserWordTestResult

COUNT_OF_TEST = 3


async def get_word(
    word_idx: int,
    user_idx: int,
    session: AsyncSession,
):
    print(word_idx, user_idx)
    stmt = (
        select(WordsToLearn)
        .where(WordsToLearn.word_id == word_idx)
        .where(WordsToLearn.user_id == user_idx)
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
        stmt = WordsToLearn(user_id=user["id"], word_id=word.id)
        await session.delete(stmt)

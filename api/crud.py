from sqlalchemy import select, join, func
from sqlalchemy.ext.asyncio import AsyncSession
from api.models import Word, LearnedWord
from api.schemas import WordSchemas
from auth.crud import get_user


async def get_10_books(session: AsyncSession):

    stmt = (
        select(Word)
        .select_from(join(Word, LearnedWord))
        .where(LearnedWord.word_id.is_(None))
        .limit(10)
    )
    result = await session.scalars(stmt)
    return result.all()


async def get_word_learned(
    word: WordSchemas, user_email: str, session: AsyncSession
) -> None:
    user = await get_user(user_email, session)
    learned_word = LearnedWord(
        user_id=user.id,
        word_id=word.id,
    )
    session.add(learned_word)
    await session.commit()


async def get_count_learned_word(user_email: str, session: AsyncSession) -> int:
    user = await get_user(user_email, session)
    stmt = select(func.count()).where(LearnedWord.user_id == user.id)
    result = await session.execute(stmt)
    return result.scalar()

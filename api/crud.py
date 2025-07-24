from sqlalchemy import select, join, func, exists
from sqlalchemy.ext.asyncio import AsyncSession
from api.models import Word, LearnedWord
from api.schemas import WordSchemas
from auth.crud import get_user


async def get_10_books(skip: int, user_email: str, session: AsyncSession):
    user = await get_user(user_email, session)
    subquery = select(1).where(
        LearnedWord.word_id == Word.id, LearnedWord.user_id == user.id
    )
    stmt = (
        select(Word).where(~exists(subquery)).order_by(Word.id).offset(skip).limit(10)
    )
    result = await session.scalars(stmt)
    words = result.all()
    return words


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


async def add_new_word(word: str, session: AsyncSession):
    stmt = Word(word=word)
    session.add(stmt)
    await session.commit()


async def update_word_db(update_data: WordSchemas, session: AsyncSession):
    stmt = select(Word).where(Word.word == update_data.word)

    word_to_update = await session.scalar(stmt)

    word_to_update.translate_ru = (
        update_data.translate_ru
        if update_data.translate_ru
        else word_to_update.translate_ru
    )

    word_to_update.translate_az = (
        update_data.translate_az
        if update_data.translate_az
        else word_to_update.translate_az
    )
    await session.commit()
    return word_to_update

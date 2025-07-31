from typing import Sequence
from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession
from api.models import Word, LearnedWord
from api.schemas import WordSchemas, BaseWord
from auth.crud import get_user


async def get_10_books(
    skip: int, user_email: str, session: AsyncSession
) -> Sequence[Word]:
    """
    get 10 random words which is not learned
    """
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


async def add_word_learned(
    word: WordSchemas, user_email: str, session: AsyncSession
) -> None:
    """
    add word to learned table
    """
    user = await get_user(user_email, session)
    learned_word = LearnedWord(
        user_id=user.id,
        word_id=word.id,
    )
    session.add(learned_word)
    await session.commit()


async def add_new_word(word: BaseWord, session: AsyncSession) -> None:
    """
    add new word
    """
    stmt = Word(
        word=word.word,
        translate_ru=word.translate_ru,
        translate_az=word.translate_az,
    )
    session.add(stmt)
    await session.commit()


async def update_word_db(update_data: WordSchemas, session: AsyncSession) -> None:
    """
    add translate for word
    """
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

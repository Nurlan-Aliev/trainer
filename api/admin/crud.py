from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from api.models import Word
from api import schemas


async def get_word(idx: int, session: AsyncSession)->Word:
    stmt = select(Word).where(Word.id == idx)
    word = await session.scalar(stmt)
    return word


async def add_new_word(word: schemas.BaseWord, session: AsyncSession) -> None:
    """
    add new word
    """
    stmt = Word(
        word_en=word.word_en,
        word_ru=word.word_ru,
        word_az=word.word_az,
    )
    session.add(stmt)
    await session.commit()


async def update_word_db(
    update_data: schemas.WordSchemas, session: AsyncSession
) -> Word:
    """
    add translate for word
    """
    stmt = select(Word).where(Word.word_en == update_data.word_en)
    word_to_update = await session.scalar(stmt)
    word_to_update.word_ru = (
        update_data.word_ru if update_data.word_ru else word_to_update.word_ru
    )
    word_to_update.word_az = (
        update_data.word_az if update_data.word_az else word_to_update.word_az
    )
    await session.commit()

    return word_to_update


async def delete_word(word: schemas.WordSchemas, session: AsyncSession):
    word_obj = await session.scalar(select(Word).where(Word.id == word.id))
    if word_obj:
        await session.delete(word_obj)
        await session.commit()

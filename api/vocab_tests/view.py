from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from api.vocab_tests import crud
from api.vocab_tests.my_enum import Test
from api.vocab_tests import schemas

from auth.validator import is_current_token
from database import db_helper


router = APIRouter(tags=["vocab_test"])


@router.post("/test")
async def make_vocab_test(
    answer: schemas.TestSchema,
    test_type: Test,
    user: dict | None = Depends(is_current_token),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    user_word_link = await crud.get_word(answer.id, user["id"], session)
    if not user_word_link:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    if answer.answer.lower() == user_word_link.word.word:
        return await crud.add_test_in_db(user_word_link.word, user, test_type, session)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.get("/to_learn")
async def get_10_words_for_test(
    test_type: Test,
    user: dict = Depends(is_current_token),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """
    Get 10 words to learn
    :return: list of 10 words for test
    """
    word_list = await crud.get_10_word_for_learn(user.get("email"), test_type, session)
    data = [
        schemas.ConstructorSchema(
            id=to_learn.word_id,
            word=to_learn.word.word,
            translate_az=to_learn.word.translate_az,
            translate_ru=to_learn.word.translate_ru,
        )
        for to_learn in word_list
    ]
    return data

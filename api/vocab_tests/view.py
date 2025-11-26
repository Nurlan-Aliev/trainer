from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from api.vocab_tests import crud
from api.vocab_tests.word_test_enum import Test
from api.vocab_tests import schemas
from api.vocab_tests.utils import (
    crete_question_and_options,
)

from auth.validator import is_current_access_token
from database import db_helper


router = APIRouter(tags=["vocab_test"])


@router.post("/test")
async def make_vocab_test(
    data: schemas.TestSchema,
    test_type: Test,
    user: dict | None = Depends(is_current_access_token),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    word_data = await crud.get_word(data.word_id, user["id"], session)
    if not word_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    if test_type == Test.rev_translate:
        correct_word = word_data.word.word_ru
    else:
        correct_word = word_data.word.word_en

    if data.user_answer.lower() == correct_word:
        await crud.add_test_in_db(word_data.word, user, test_type, session)
    return correct_word


@router.get("/constructor")
async def get_10_words_for_test(
    user: dict = Depends(is_current_access_token),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """
    Get 10 words to learn
    :return: list of 10 words for test
    """
    word_list = await crud.get_10_word_for_learn(user, Test.constructor.value, session)
    data = [
        schemas.ConstructorSchema(
            word_id=to_learn.word_id,
            word_az=to_learn.word.word_az,
            word_ru=to_learn.word.word_ru,
        )
        for to_learn in word_list
    ]
    return data


@router.get("/translate")
async def get_words_translate(
    user: dict = Depends(is_current_access_token),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    word_list = await crud.get_10_word_for_learn(user, Test.translate.value, session)
    options = await crud.get_random_words(len(word_list), session)
    return crete_question_and_options(list(word_list), options, Test.translate.value)


@router.get("/rev_translate")
async def get_words_reverse_translate(
    user: dict = Depends(is_current_access_token),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    word_list = await crud.get_10_word_for_learn(
        user, Test.rev_translate.value, session
    )
    options = await crud.get_random_words(len(word_list), session)
    return crete_question_and_options(
        list(word_list), options, Test.rev_translate.value
    )

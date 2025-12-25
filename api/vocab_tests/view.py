from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from api.vocab_tests import crud_learned
from api.vocab_tests import crud
from api.vocab_tests.custom_enum import Test
from api.vocab_tests import schemas
from api.vocab_tests.utils import (
    crete_question_and_options,
)

from auth.validator import is_current_access_token
from database import db_helper


router = APIRouter(tags=["vocab_test"])


@router.get("/constructor")
async def get_constructor(
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


@router.post('/constructor')
async def post_constructor(
    data: schemas.TestSchema,
    user: dict | None = Depends(is_current_access_token),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    word = (await crud.get_word(data.word_id, user["id"], session)).word
    if not word:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    if data.user_answer.lower() == word.word_en:
        await crud.add_test_in_db(word, user, Test.constructor.value, session)
    return word.word_en


@router.get("/rev_translate")
async def get_words_translate(
    user: dict = Depends(is_current_access_token),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    word_list = await crud.get_10_word_for_learn(user, Test.translate.value, session)
    options = await crud.get_random_words(len(word_list), session)
    return crete_question_and_options(list(word_list), options, Test.translate.value)


@router.post("/rev_translate")
async def post_translate(
    data: schemas.TestSchema,
    user: dict | None = Depends(is_current_access_token),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    word = (await crud.get_word(data.word_id, user["id"], session)).word
    if not word:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    if data.user_answer.lower() == word.word_en:
        await crud.add_test_in_db(word, user, Test.translate.value, session)

    return word.word_en


@router.get("/translate")
async def get_rev_translate(
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


@router.post("/translate")
async def post_rev_translate(
    data: schemas.TestSchema,
    user: dict | None = Depends(is_current_access_token),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    word = (await crud.get_word(data.word_id, user["id"], session)).word
    if not word:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    correct_word = getattr(word, data.language.value)
    if data.user_answer.lower() == correct_word:
        await crud.add_test_in_db(word, user, Test.rev_translate.value, session)
    return correct_word


@router.get("/remember")
async def get_words_reverse_translate(
    user: dict = Depends(is_current_access_token),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    word_list = await crud.get_10_word_for_learn(user,Test.remember.value, session)

    data = [
        schemas.ConstructorSchema(
            word_id=to_learn.word_id,
            word_en=to_learn.word.word_en,
            word_az=to_learn.word.word_az,
            word_ru=to_learn.word.word_ru,
        )
        for to_learn in word_list
    ]
    return data


@router.post("/remember")
async def forgot_word(
    data: schemas.Remember,
    user: dict = Depends(is_current_access_token),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    word = (await crud.get_word(data.word_id, user["id"], session)).word

    if data.remember:
        await crud.add_test_in_db(word, user, Test.constructor.value, session)
    return {'word_ru': word.learned_word.word_ru, 'word_az': word.learned_word.word_az}

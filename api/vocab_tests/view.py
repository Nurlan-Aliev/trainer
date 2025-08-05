from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from api.vocab_tests import crud
from api.vocab_tests.my_enum import Test
from api.vocab_tests.schemas import TestSchema
from auth.validator import is_current_token
from database import db_helper


router = APIRouter(tags=["vocab_test"])


@router.post("/test")
async def make_vocab_test(
    answer: TestSchema,
    test_type: Test,
    user: dict | None = Depends(is_current_token),
    session: AsyncSession = Depends(db_helper.session_dependency),
):

    word = await crud.get_word(answer.id, user["id"], session)
    if not word:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    if answer.answer == word.word:
        return await crud.add_test_in_db(word.word, user, test_type, session)

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

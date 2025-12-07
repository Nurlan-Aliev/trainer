from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api import crud, schemas
from api.admin import crud
from auth.permissions import is_admin
from database import db_helper


router = APIRouter(
    tags=["admin"],
    dependencies=[Depends(is_admin)],
)


@router.post("/word")
async def add_word(
    word: schemas.BaseWord,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """
    add a new words in the list
    """
    await crud.add_new_word(word, session)
    return "word added"


@router.patch("/word")
async def update_word(
    update_data: schemas.WordSchemas,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """
    update words
    """
    word = await crud.update_word_db(update_data, session)
    return word


@router.delete("/word")
async def delete_word(
    update_data: schemas.WordSchemas,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    await crud.delete_word(update_data, session)

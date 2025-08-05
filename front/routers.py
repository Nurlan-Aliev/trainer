from fastapi import APIRouter
from front.view import router as main_front_router
from front.auth_front import router as auth_router
from front.learn_words_view import router as lern_word


router = APIRouter()


router.include_router(main_front_router)
router.include_router(auth_router)
router.include_router(lern_word)

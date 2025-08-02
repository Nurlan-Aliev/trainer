from fastapi import APIRouter
from front.view import router as main_front_router
from front.auth_front import router as auth_router

router = APIRouter()


router.include_router(main_front_router)
router.include_router(auth_router)

from fastapi import APIRouter
from api.view import router as api_router
from api.vocab_tests.view import router as vocab_tests_router
from api.admin.view import router as admin_routers

router = APIRouter()


router.include_router(api_router)
router.include_router(vocab_tests_router)
router.include_router(admin_routers, prefix="/admin")

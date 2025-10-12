from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from api.routers import router as api_router
from auth.views import router as auth_router
from config import settings


app = FastAPI(openapi_url="/openapi.json" if settings.DEBUG else None)
app.include_router(api_router, prefix="/api")
app.include_router(auth_router, prefix="/auth", tags=["login"])


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

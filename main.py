from fastapi import FastAPI
from starlette.staticfiles import StaticFiles


from api.routers import router as api_router
from auth.views import router as auth_router
from front.routers import router as front_router

app = FastAPI(openapi_url=None)
app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(api_router, prefix="/api")
app.include_router(auth_router, prefix="/auth", tags=["login"])
app.include_router(front_router, tags=["front"])

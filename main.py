from fastapi import FastAPI, Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from api.view import router as api_router
from auth.views import router as auth_router


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(api_router, prefix="/api")
app.include_router(auth_router, prefix="/auth")

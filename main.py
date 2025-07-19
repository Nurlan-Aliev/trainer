from fastapi import FastAPI, Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

db = [
    {'en': 'word1', 'ru':'слово1', 'az':'söz1'},
    {'en': 'word2', 'ru':'слово2', 'az':'söz2'},
    {'en': 'word3', 'ru':'слово3', 'az':'söz3'},
    {'en': 'word4', 'ru':'слово4', 'az':'söz4'},
]


@app.get("/")
def get_home_page(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "word": {
                "learned": 25,
                'word': db
            },
        },
    )

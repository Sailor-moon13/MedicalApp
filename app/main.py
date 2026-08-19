from fastapi import FastAPI, Request
from app.routers.predict import router
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
app = FastAPI(
    title="Medical AI",
    version="1.0"
    )

app.include_router(router)

# Подключаем папку со статикой
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Подключаем шаблоны
templates = Jinja2Templates(directory="app/templates")


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
    name="index.html",
    request=request
    )
from fastapi import FastAPI, Request
from database import models
from database.data_base import engine
from api import auth_api, movies_api, favorites_api, ratings_api, stats_api
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import HTMLResponse


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Movie Library")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

templates = Jinja2Templates(directory="templates")

app.include_router(auth_api.router, tags=["Auth"])
app.include_router(movies_api.router, prefix="/movies", tags=["Movies"])
app.include_router(favorites_api.router, prefix="/favorites", tags=["Favorites"])
app.include_router(ratings_api.router, prefix="/ratings", tags=["Ratings"])
app.include_router(stats_api.router, prefix="/stats", tags=["Stats"])


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})



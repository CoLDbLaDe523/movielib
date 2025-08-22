from fastapi import FastAPI, Request, Depends
from sqlalchemy.orm import Session
from database import models, data_base
from database.data_base import engine
from api import auth_api, movies_api, favorites_api, ratings_api, stats_api
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from api.auth_api import get_current_user
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi import Response

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
async def read_index(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse("index.html", {"request": request, "user": user})


@app.get("/profile", response_class=HTMLResponse)
async def profile(request: Request, db: Session = Depends(data_base.get_db), user=Depends(get_current_user)):
    if not user:
        return templates.TemplateResponse("profile.html", {"request": request, "error": "Сначала войдите!"})
    return templates.TemplateResponse("profile.html", {"request": request, "user": user})


@app.get("/auth/me")
async def auth_me(token: str = Depends(oauth2_scheme)):
    # тут нужно проверить токен / куки
    # для простоты можно заглушку сделать
    if token:
        return {"logged_in": True, "username": "DemoUser"}
    return JSONResponse(status_code=401, content={"logged_in": False})

@app.post("/logout")
def logout(response: Response):
    response.delete_cookie("token")
    return RedirectResponse("/", status_code=303)



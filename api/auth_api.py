from fastapi import APIRouter, Depends, HTTPException, status, Form, Response, Request
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse, HTMLResponse
from database import models, data_base
from api import utils_api
from pydantic import BaseModel
from jose import JWTError, jwt
from urllib.parse import quote
from fastapi.templating import Jinja2Templates


router = APIRouter()

templates = Jinja2Templates(directory="templates")


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_current_user(request: Request, db: Session = Depends(data_base.get_db)):
    token = request.cookies.get("access_token")
    if not token:
        return None
    try:
        payload = jwt.decode(token, utils_api.SECRET_KEY, algorithms=[utils_api.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
    except JWTError:
        return None

    return get_user_by_username(db, username=username)


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/register")
def register(
        username: str = Form(...),
        email: str = Form(...),
        password: str = Form(...),
        db: Session = Depends(data_base.get_db)
):
    db_user = get_user_by_username(db, username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = utils_api.get_password_hash(password)
    new_user = models.User(username=username, email=email, hashed_password=hashed_password, role="user")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = utils_api.create_access_token(data={"sub": new_user.username})

    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(key="access_token", value=access_token, httponly=True, samesite="lax")
    response.set_cookie(key="username", value=new_user.username)

    flash_message = quote("Регистрация прошла успешно!")
    response.set_cookie(key="flash_message", value=flash_message, max_age=5)

    return response


@router.post("/login")
def login(
        username: str = Form(...),
        password: str = Form(...),
        db: Session = Depends(data_base.get_db)
):
    user = get_user_by_username(db, username)
    if not user or not utils_api.verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = utils_api.create_access_token(data={"sub": user.username})
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(key="access_token", value=access_token, httponly=True, max_age=60*60*24, samesite="lax")
    response.set_cookie(key="username", value=user.username)
    return response


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse("login.html", {"request": request, "user": user})


@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse("register.html", {"request": request, "user": user})


@router.get("/logout")
def logout():
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("access_token")
    response.delete_cookie("username")
    return response


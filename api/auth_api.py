from fastapi import APIRouter, Depends, HTTPException, Form, Response, Request
from sqlalchemy.orm import Session
from database import models, data_base
from api import utils_api
from jose import JWTError, jwt
from fastapi.responses import JSONResponse


router = APIRouter()


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


@router.post("/register")
def register(
        username: str = Form(...),
        email: str = Form(...),
        password: str = Form(...),
        db: Session = Depends(data_base.get_db)
):
    db_user = get_user_by_username(db, username)
    if db_user:
        raise HTTPException(status_code=400, detail="Пользователь с таким именем уже зарегистрирован")

    hashed_password = utils_api.get_password_hash(password)
    new_user = models.User(username=username, email=email, hashed_password=hashed_password, role="user")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = utils_api.create_access_token(data={"sub": new_user.username})

    return JSONResponse(
        status_code=201,
        content={
            "message": "Аккаунт успешно зарегистрирован",
            "username": new_user.username,
            "token": access_token
        }
    )


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

    return JSONResponse(
        status_code=200,
        content={
            "message": "Успешный вход",
            "username": user.username,
            "token": access_token
        }
    )


@router.post("/logout")
def logout(response: Response):
    # Удаляем куки
    response.delete_cookie("access_token")
    response.delete_cookie("username")

    return JSONResponse(
        status_code=200,
        content={"message": "Вы успешно вышли из системы"}
    )



from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import models, data_base
from api import schemas, auth_api

router = APIRouter()

@router.post("/{movie_id}")
def add_favorite(movie_id: int, db: Session = Depends(data_base.get_db), user: models.User = Depends(auth_api.get_current_user)):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    fav = models.Favorite(user_id=user.id, movie_id=movie_id)
    db.add(fav)
    db.commit()
    return {"msg": "Added to favorites"}

@router.get("/", response_model=list[schemas.Favorite])
def list_favorites(db: Session = Depends(data_base.get_db), user: models.User = Depends(auth_api.get_current_user)):
    return db.query(models.Favorite).filter(models.Favorite.user_id == user.id).all()

@router.delete("/{movie_id}")
def remove_favorite(movie_id: int, db: Session = Depends(data_base.get_db), user: models.User = Depends(auth_api.get_current_user)):
    fav = db.query(models.Favorite).filter(models.Favorite.user_id == user.id, models.Favorite.movie_id == movie_id).first()
    if not fav:
        raise HTTPException(status_code=404, detail="Favorite not found")
    db.delete(fav)
    db.commit()
    return {"msg": "Removed from favorites"}
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import schemas, auth_api
from database import data_base, models
router = APIRouter()

@router.get("/", response_model=list[schemas.Movie])
def list_movies(db: Session = Depends(data_base.get_db)):
    return db.query(models.Movie).all()

@router.post("/", response_model=schemas.Movie)
def create_movie(movie: schemas.MovieCreate, db: Session = Depends(data_base.get_db), user: models.User = Depends(auth_api.get_current_user)):
    db_movie = models.Movie(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

@router.get("/{movie_id}", response_model=schemas.Movie)
def get_movie(movie_id: int, db: Session = Depends(data_base.get_db)):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@router.put("/{movie_id}", response_model=schemas.Movie)
def update_movie(movie_id: int, updated: schemas.MovieCreate, db: Session = Depends(data_base.get_db), user: models.User = Depends(auth_api.get_current_user)):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    for key, value in updated.dict().items():
        setattr(movie, key, value)
    db.commit()
    db.refresh(movie)
    return movie

@router.delete("/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(data_base.get_db), user: models.User = Depends(auth_api.get_current_user)):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    db.delete(movie)
    db.commit()
    return {"msg": "Movie deleted"}

@router.get("/search/")
def search_movies(query: str, db: Session = Depends(data_base.get_db)):
    return db.query(models.Movie).filter(models.Movie.title.contains(query) | models.Movie.genre.contains(query)).all()
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import schemas, auth_api
from database import models, data_base
router = APIRouter()

@router.post("/{movie_id}")
def rate_movie(movie_id: int, rating: schemas.RatingCreate, db: Session = Depends(data_base.get_db), user: models.User = Depends(auth_api.get_current_user)):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    new_rating = models.Rating(user_id=user.id, movie_id=movie_id, score=rating.score)
    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)
    return new_rating

@router.get("/{movie_id}")
def get_ratings(movie_id: int, db: Session = Depends(data_base.get_db)):
    ratings = db.query(models.Rating).filter(models.Rating.movie_id == movie_id).all()
    if not ratings:
        raise HTTPException(status_code=404, detail="No ratings yet")
    avg_score = sum(r.score for r in ratings) / len(ratings)
    return {"ratings": ratings, "average": avg_score}
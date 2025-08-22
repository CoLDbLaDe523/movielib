from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import models, data_base

router = APIRouter()

@router.get("/")
def get_stats(db: Session = Depends(data_base.get_db)):
    users_count = db.query(models.User).count()
    movies_count = db.query(models.Movie).count()
    top_movies = (
        db.query(models.Movie.title, models.Rating.score)
        .join(models.Rating)
        .all()
    )
    # Подсчёт среднего рейтинга фильмов
    movie_scores = {}
    for title, score in top_movies:
        movie_scores.setdefault(title, []).append(score)
    top_avg = sorted([(t, sum(s) / len(s)) for t, s in movie_scores.items()], key=lambda x: x[1], reverse=True)[:3]
    return {"users": users_count, "movies": movies_count, "top_movies": top_avg}
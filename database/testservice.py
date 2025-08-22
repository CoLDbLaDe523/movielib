from sqlalchemy import func
from database.data_base import get_db
from database.models import Movie, Rating

# Функция для создания фильма
def create_movie(title: str, genre: str, description: str = None):
    db = next(get_db())  # Подключение к БД

    new_movie = Movie(title=title, genre=genre, description=description)
    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)  # чтобы получить id и свежие данные из БД
    return new_movie

# Функция для получения первых двадцати фильмов
def get_movies_db():
    db = next(get_db())
    all_movies = db.query(Movie).limit(20).all()
    return all_movies

# Функция для получения топ 10 фильмов
def get_top_10_rating_db():
    db = next(get_db())

    top_10 = (
        db.query(
            Movie.id,
            Movie.title,
            func.avg(Rating.score).label("avg_score")
        )
        .join(Rating, Rating.movie_id == Movie.id)   # соединяем Movie и Rating
        .group_by(Movie.id)                          # группируем по фильму
        .order_by(func.avg(Rating.score).desc())     # сортировка по среднему рейтингу
        .limit(10)                                   # топ 10
        .all()
    )

    return top_10

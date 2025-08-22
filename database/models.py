from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(24), unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True)
    role = Column(String, default="user")
    phonenumber = Column(String, nullable=True)
    reg_date = Column(DateTime , default=datetime.now())
    hashed_password = Column(String, nullable=False)

    favorites = relationship("Favorite", back_populates="user")
    ratings = relationship("Rating", back_populates="user")

class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True)
    genre = Column(String, index=True)
    description = Column(String)

    favorites = relationship("Favorite", back_populates="movie")
    ratings = relationship("Rating", back_populates="movie")

class Favorite(Base):
    __tablename__ = "favorites"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    movie_id = Column(Integer, ForeignKey("movies.id"))

    user = relationship("User", back_populates="favorites")
    movie = relationship("Movie", back_populates="favorites")

class Rating(Base):
    __tablename__ = "ratings"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    movie_id = Column(Integer, ForeignKey("movies.id"))
    score = Column(Float)

    user = relationship("User", back_populates="ratings")
    movie = relationship("Movie", back_populates="ratings")


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", backref="sessions")

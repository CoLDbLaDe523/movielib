from pydantic import BaseModel
from typing import Optional, List

class UserCreate(BaseModel):
    username: str
    password: str
    phonenumber: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class MovieBase(BaseModel):
    title: str
    genre: str
    description: Optional[str] = None

class MovieCreate(MovieBase):
    pass

class Movie(MovieBase):
    id: int
    class Config:
        orm_mode = True

class Favorite(BaseModel):
    id: int
    movie: Movie
    class Config:
        orm_mode = True

class RatingCreate(BaseModel):
    score: float

class Rating(BaseModel):
    id: int
    score: float
    movie: Movie
    class Config:
        from_attributes = True

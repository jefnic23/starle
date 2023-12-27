from pydantic import BaseModel


class Movie(BaseModel):
    title: str
    release_year: int
    poster_path: str


class Starle(BaseModel):
    name: str
    gender: str
    movies: list[Movie]

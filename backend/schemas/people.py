from datetime import date
from typing import Optional, Union

from pydantic import BaseModel

from backend.enums import Gender


class KnownFor(BaseModel):
    adult: bool
    backdrop_path: Optional[str]
    id: int
    original_language: str
    overview: str
    poster_path: Optional[str]
    media_type: str
    genre_ids: list[int]
    popularity: float
    vote_average: float
    vote_count: int


class Movie(KnownFor):
    title: str
    original_title: str
    release_date: date
    video: bool


class Tv(KnownFor):
    name: str
    original_name: str
    first_air_date: date
    origin_country: list[str]


class Person(BaseModel):
    adult: bool
    id: int
    name: str
    original_name: str
    media_type: str
    popularity: float
    gender: Gender
    known_for_department: str
    profile_path: Optional[str]
    known_for: list[Union[Movie, Tv]]


class TmdbResponse(BaseModel):
    page: int
    results: list[Person]

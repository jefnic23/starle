from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, validator

from backend.enums import Genre


class MemberBase(BaseModel):
    adult: bool
    backdrop_path: Optional[str] = None
    credit_id: str
    genre_ids: list[Genre]
    id: int
    original_language: str
    original_title: str
    overview: Optional[str] = None
    popularity: float
    poster_path: Optional[str] = None
    release_date: Optional[date] = None
    title: str
    video: bool
    vote_average: float
    vote_count: int

    @validator("release_date", pre=True, always=True)
    def parse_date(cls, value):
        if not value:
            return None
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            return None


class CastMember(MemberBase):
    character: str
    order: int


class CrewMember(MemberBase):
    department: str
    job: str


class Credits(BaseModel):
    cast: list[CastMember]
    crew: list[CrewMember]
    id: int

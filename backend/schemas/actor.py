from pydantic import BaseModel


class Actor(BaseModel):
    id: int
    name: str
    gender: str
    popularity: float

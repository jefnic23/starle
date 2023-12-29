from fastapi import APIRouter

from backend.schemas.starle import Starle
from backend.services.db import get_actor_names
from backend.services.game import create_game

router = APIRouter()


@router.get("/api/starle")
async def get_game(seed: int) -> list[Starle]:
    return await create_game(seed)


@router.get("/api/names")
def get_names() -> list[str]:
    return get_actor_names()

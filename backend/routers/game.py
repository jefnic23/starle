from fastapi import APIRouter

from backend.schemas.starle import Starle
from backend.services.starle import create_game

router = APIRouter()


@router.get("/api/starle")
async def get_game() -> list[Starle]:
    return await create_game()

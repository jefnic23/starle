from fake_useragent import UserAgent

from backend.config import settings
from backend.schemas.people import Person, TmdbResponse
from backend.services.http_client import get_async


async def get_trending_people() -> TmdbResponse:
    """Get the trending people on TMDB."""

    headers = {
        "User-Agent": UserAgent().random,
        "Authorization": f"Bearer {settings.API_READ_ACCESS_TOKEN}",
    }

    url = "https://api.themoviedb.org/3/trending/person/day?language=en-US"
    req = await get_async(url, headers)
    if req:
        return TmdbResponse(**req)
    else:
        print("Error getting game data")
        return None


def filter_actors(people: list[Person]) -> list[Person]:
    return [
        person
        for person in people
        if person.known_for_department == "Acting"
        and not any(known_for.media_type == "tv" for known_for in person.known_for)
        and not any(known_for.poster_path is None for known_for in person.known_for)
    ]

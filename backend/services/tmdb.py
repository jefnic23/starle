from fake_useragent import UserAgent

from backend.config import settings
from backend.enums import MovieExclusiveGenres
from backend.schemas.credits import CastMember, Credits
from backend.services.http_client import get_async

MOVIE_EXCLUSIVE_GENRES = [genre.value for genre in MovieExclusiveGenres]


async def get_filtered_movies(actor_id: int) -> list[CastMember]:
    """Asynchronously retrieve and return a filtered list of movies for a given actor ID."""
    movies = await _get_movie_credits(actor_id)
    return _filter_movies(movies.cast)


async def _get_movie_credits(actor_id: int) -> Credits:
    """Asynchronously retrieve and return movie credits for a given actor ID, handling errors appropriately."""
    headers = {
        "User-Agent": UserAgent().random,
        "Authorization": f"Bearer {settings.API_READ_ACCESS_TOKEN}",
    }

    url = f"https://api.themoviedb.org/3/person/{actor_id}/movie_credits?language=en-US"
    req = await get_async(url, headers)
    if req:
        return Credits(**req)
    else:
        print("Error getting game data")
        return None


def _filter_movies(movies: list[CastMember]) -> list[CastMember]:
    """Filter movies based on specified criteria like non-adult, non-video, release date, poster, popularity, and genre."""
    return [
        movie
        for movie in movies
        if movie.adult is False
        and movie.video is False
        and movie.release_date
        and movie.poster_path
        and movie.popularity >= 20.0
        and all(
            genre_id.value in MOVIE_EXCLUSIVE_GENRES for genre_id in movie.genre_ids
        )
    ]

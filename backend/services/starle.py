from backend.schemas.starle import Movie, Starle
from backend.services.tmdb import filter_actors, get_trending_people


async def create_game() -> list[Starle]:
    tmbd_response = await get_trending_people()

    actors = filter_actors(tmbd_response.results)

    starles = []
    for actor in actors:
        # Filter out 'tv' media types
        movies = [
            Movie(
                title=movie.title,
                release_year=movie.release_date.year,
                poster_path=f"https://image.tmdb.org/t/p/original{movie.poster_path}",
            )
            for movie in actor.known_for
        ]

        # If there are no movies, skip this result item
        if not movies:
            continue

        # Create a Starle instance
        starle = Starle(
            name=actor.name,
            gender=actor.gender.name,
            movies=movies,
        )
        starles.append(starle)

    return starles

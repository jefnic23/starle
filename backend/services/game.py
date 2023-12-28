import random

from backend.schemas.starle import Movie, Starle
from backend.services.db import get_actors
from backend.services.tmdb import get_filtered_movies


async def create_game(seed: int) -> list[Starle]:
    """Asynchronously create a game with unique Starle instances based on actors and their popular movies, using a seed for randomness."""
    actors = get_actors()

    while True:
        # random.seed(seed)
        filtered_actors = random.choices(
            actors, weights=[actor.popularity for actor in actors], k=6
        )

        if len(set([actor.id for actor in filtered_actors])) == 6:
            break

    starles = []

    for actor in filtered_actors:
        filtered_movies = await get_filtered_movies(actor.id)

        while True:
            # random.seed(seed)
            movies = sorted(
                random.choices(
                    filtered_movies,
                    weights=[movie.popularity for movie in filtered_movies],
                    k=3,
                ),
                key=lambda movie: movie.popularity,
                reverse=True,
            )

            if len(set([movie.id for movie in movies])) == 3:
                break

        starle = Starle(
            name=actor.name,
            gender=actor.gender,
            movies=[
                Movie(
                    title=movie.title,
                    release_year=movie.release_date.year,
                    poster_path=f"https://image.tmdb.org/t/p/original{movie.poster_path}",
                )
                for movie in movies
            ],
        )

        starles.append(starle)

    return starles

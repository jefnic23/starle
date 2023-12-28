import numpy as np
from numpy.typing import NDArray, float

from backend.schemas.starle import Movie, Starle
from backend.services.db import get_actors
from backend.services.tmdb import get_filtered_movies


async def create_game(seed: int) -> list[Starle]:
    """Asynchronously create a game with unique Starle instances based on actors and their popular movies, using a seed for randomness."""
    actors = get_actors()

    starles = []

    # TODO: if an actor doesn't have 3 movies, remove them from the list

    np.random.default_rng(seed=seed)
    filtered_actors = np.random.choice(
        actors,
        size=6,
        replace=False,
        p=_get_weights([actor.popularity for actor in actors]),
    )

    for actor in filtered_actors:
        filtered_movies = await get_filtered_movies(actor.id)

        np.random.default_rng(seed=seed)
        movies = sorted(
            np.random.choice(
                filtered_movies,
                size=3,
                replace=False,
                p=_get_weights([movie.popularity for movie in filtered_movies]),
            ),
            key=lambda movie: movie.popularity,
            reverse=True,
        )

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


def _get_weights(population: list[float]) -> NDArray[float]:
    probability = np.array(population)
    return probability / probability.sum()

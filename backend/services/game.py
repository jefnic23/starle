from typing import Any

import numpy as np
from numpy.typing import NDArray

from backend.schemas.starle import Movie, Starle
from backend.services.db import get_actors, update_actor
from backend.services.tmdb import get_filtered_movies


async def create_game(seed: int) -> list[Starle]:
    """Asynchronously create a game with unique Starle instances based on actors and their popular movies, using a seed for randomness."""
    actors = get_actors()

    starles = []

    rng = np.random.default_rng(seed=seed)

    while len(starles) < 6:
        filtered_actors = rng.choice(
            actors,
            size=6,
            replace=False,
            p=_get_weights([actor.popularity for actor in actors]),
        )

        for actor in filtered_actors:
            filtered_movies = await get_filtered_movies(actor.id)

            if len(filtered_movies) < 3:
                actor.viable = 0
                update_actor(actor)
                actors = [actor for actor in actors if actor.viable == 1]
                continue

            movies = sorted(
                rng.choice(
                    filtered_movies,
                    size=3,
                    replace=False,
                    p=_get_weights([movie.vote_count for movie in filtered_movies]),
                ),
                key=lambda movie: movie.vote_count,
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


def _get_weights(population: list[float]) -> NDArray[Any]:
    """Calculate and return normalized weights from a list of population values."""
    probability = np.array(population)
    return probability / probability.sum()

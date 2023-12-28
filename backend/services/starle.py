import random
import sqlite3
from contextlib import closing
from typing import Any

from backend.schemas.actor import Actor
from backend.schemas.starle import Movie, Starle
from backend.services.tmdb import filter_movies, get_movie_credits


async def create_game() -> list[Starle]:
    with closing(sqlite3.connect("backend/actors.db")) as connection:
        with closing(connection.cursor()) as cursor:
            rows = cursor.execute("SELECT * FROM actors").fetchall()
            actors = [Actor(**_row_to_dict(row, cursor)) for row in rows]

    while True:
        filtered_actors = random.choices(
            actors, weights=[actor.popularity for actor in actors], k=6
        )

        if len(set([actor.id for actor in filtered_actors])) == 6:
            break

    starles = []

    for actor in filtered_actors:
        movie_credits = await get_movie_credits(actor.id)

        filtered_movies = filter_movies(movie_credits.cast)

        while True:
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


def _row_to_dict(row: Any, cursor: sqlite3.Cursor):
    """Convert a database row to a dictionary keyed by column names."""
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))

import sqlite3
from contextlib import closing
from functools import lru_cache
from typing import Any

from backend.schemas.actor import Actor


@lru_cache()
def get_actors() -> list[Actor]:
    """Retrieve a cached list of all actors from the `actors` table in the SQLite database."""
    with closing(sqlite3.connect("backend/starle.db")) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.row_factory = _actor_factory
            return cursor.execute("SELECT * FROM actors WHERE viable = 1").fetchall()


def update_actor(actor: Actor) -> None:
    """Update the `viable` status of an actor in the database."""
    with closing(sqlite3.connect("backend/starle.db")) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute(
                "UPDATE actors SET viable = ? WHERE id = ?", (actor.viable, actor.id)
            )
            connection.commit()


def _actor_factory(cursor: sqlite3.Cursor, row: Any) -> Actor:
    """Create an Actor instance from a database row using cursor metadata."""
    columns = [col[0] for col in cursor.description]
    return Actor(**dict(zip(columns, row)))

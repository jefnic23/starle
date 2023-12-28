from functools import lru_cache
import sqlite3
from contextlib import closing
from typing import Any

from backend.schemas.actor import Actor


@lru_cache()
def get_actors() -> list[Actor]:
    """Retrieve a cached list of all actors from the `actors` table in the SQLite database."""
    with closing(sqlite3.connect("backend/starle.db")) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.row_factory = _actor_factory
            return cursor.execute("SELECT * FROM actors").fetchall()


def _actor_factory(cursor: sqlite3.Cursor, row: Any) -> Actor:
    """Create an Actor instance from a database row using cursor metadata."""
    columns = [col[0] for col in cursor.description]
    return Actor(**dict(zip(columns, row)))

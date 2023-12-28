from functools import lru_cache
import sqlite3
from contextlib import closing
from typing import Any

from backend.schemas.actor import Actor


@lru_cache()
def get_actors() -> list[Actor]:
    with closing(sqlite3.connect("backend/actors.db")) as connection:
        with closing(connection.cursor()) as cursor:
            rows = cursor.execute("SELECT * FROM actors").fetchall()
            return [Actor(**_row_to_dict(row, cursor)) for row in rows]


def _row_to_dict(row: Any, cursor: sqlite3.Cursor):
    """Convert a database row to a dictionary keyed by column names."""
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))

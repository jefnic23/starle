from fake_useragent import UserAgent

from backend.config import settings
from backend.enums import MovieExclusiveGenres
from backend.schemas.credits import CastMember, Credits
from backend.services.http_client import get_async

MOVIE_EXCLUSIVE_GENRES = [genre.value for genre in MovieExclusiveGenres]


async def get_filtered_movies(actor_id: int) -> list[CastMember]:
    """
    Asynchronously retrieves and filters the movie credits for a specified actor.

    This function serves as a helper that combines two key functionalities: fetching movie credits
    for a given actor and filtering these movies based on specific criteria. Firstly, it invokes
    the asynchronous `_get_movie_credits` function, passing in the actor's unique ID, to obtain
    their movie credits. These credits include various details about each movie the actor has
    participated in. The function then filters these movies by calling `_filter_movies`, which
    applies a set of predefined criteria such as filtering out adult movies, videos, movies without
    a release date or poster path, and those with a popularity score below 20.0. It also ensures
    that the movie genres match a predefined set of exclusive genres.

    Parameters:
    actor_id (int): The unique identifier for the actor whose movie credits are to be retrieved
                    and filtered.

    Returns:
    list[CastMember]: A list of `CastMember` objects representing the movies that meet the
                      filtering criteria. Each `CastMember` object contains details about a
                      specific movie. If there are no movies that meet the criteria or if the
                      actor has no movie credits, the list may be empty.

    Raises:
    - This function will propagate any exceptions raised by `_get_movie_credits` or `_filter_movies`.
    - The function depends on the external API for fetching movie credits and thus may be affected
      by network issues or API changes.

    Note:
    - The function is asynchronous and should be awaited when called.
    - The specific filtering criteria are defined within the `_filter_movies` function.
    """
    movies = await _get_movie_credits(actor_id)
    return _filter_movies(movies.cast)


async def _get_movie_credits(actor_id: int) -> Credits:
    """
    Asynchronously retrieves the movie credits for a specific actor by their ID.

    This function sends an asynchronous HTTP GET request to an external movie database API,
    specifically to fetch the movie credits associated with a given actor. The actor is
    identified by their unique actor ID. The function uses a set of headers, including a
    User-Agent for the request and an Authorization token for API access. If the request
    is successful, the response is parsed into a Credits object. If the request fails,
    an error message is printed, and the function returns None.

    Parameters:
    actor_id (int): The unique identifier for the actor whose movie credits are to be retrieved.

    Returns:
    Credits: An object containing the movie credits of the specified actor. This includes
             information about each movie the actor has been involved in. If the request fails,
             the function returns None.

    Raises:
    - Prints an error message if there is an issue with getting the data (e.g., network error,
      invalid actor ID, API issues).

    Note:
    - This function requires external API access and is dependent on the availability and
      responsiveness of the themoviedb.org API.
    - The function is asynchronous and should be awaited when called.
    """

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
    """
    Filters a list of movies based on specific criteria.

    This function iterates through a given list of movie objects (represented by the CastMember class)
    and returns a subset of those movies that meet all of the following criteria:

    1. The movie is not marked as 'adult'.
    2. The movie is not a 'video'.
    3. The movie has a release date specified.
    4. The movie has a poster path specified.
    5. The movie's popularity score is 20.0 or higher.
    6. All genre IDs associated with the movie are within a predefined set of movie-exclusive genres
       (indicated by the MOVIE_EXCLUSIVE_GENRES constant).

    Parameters:
    movies (list[CastMember]): A list of movie objects to be filtered.

    Returns:
    list[CastMember]: A list containing only the movie objects that meet all the specified criteria.
    """
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

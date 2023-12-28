from typing import Any

import aiohttp


async def get_async(url: str, headers: dict[str, Any]) -> dict[str, Any]:
    """Asynchronously perform a GET request to a URL with specified headers and return the JSON response."""
    async with aiohttp.ClientSession() as client:
        async with client.get(url, headers=headers) as res:
            if res.status not in [200, 201]:
                await res.raise_for_status()
            else:
                return await res.json()

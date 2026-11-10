from typing import Optional
import logging
import httpx
import config

logger = logging.getLogger(__name__)


async def _fetch_from_osrm(coordinates: list[tuple[float, float]], client: httpx.AsyncClient) -> Optional[tuple[list[list[float]], list[list[float]]]]:
    coords_str = ";".join(f"{lon},{lat}" for lat, lon in coordinates)
    url = f"{config.OSRM_TABLE_URL}{coords_str}"
    params = {"annotations": "duration,distance"}
    try:
        response = await client.get(url=url, params=params)
        data = response.json()
        if data.get("code") == "Ok":
            return data["durations"], data["distances"]
        else:
            logger.error("Could not build distance matrix due to error: %s (code: %s).", data.get("message"),
                         data.get("code"))
            return None
    except httpx.HTTPError:
        logger.error("Error establishing HTTP connection at the start of an OSRM API call.")
        return None
    except Exception as err:
        logger.exception("Distance matrix failed to generate for coords: %s", coordinates)
        return None

async def get_osrm_matrices(coordinates: list[tuple[float, float]], client: Optional[httpx.AsyncClient] = None) -> Optional[tuple[list[list[float]], list[list[float]]]]:
    if client is not None:
        return await _fetch_from_osrm(coordinates, client)

    async with httpx.AsyncClient() as client:
        return await _fetch_from_osrm(coordinates, client)
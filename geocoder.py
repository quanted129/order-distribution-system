from typing import Optional
import httpx
import config
import json
import logging

logger = logging.getLogger(__name__)


async def _fetch_from_geocoder(address: str, client: Optional[httpx.AsyncClient] = None) -> Optional[tuple[float, float]]:
    base_url = config.YANDEX_GEOCODER_URL
    query_params = {
        "apikey": config.YANDEX_API_KEY,
        "geocode": address if "беларусь" in address.lower() else f"Беларусь, {address}",
        "format": "json"
    }

    try:
        response = await client.get(base_url, params=query_params)
        response.raise_for_status()
        data = response.json()
        print(json.dumps(data, indent=2))  # temporary logging
        members = data["response"]["GeoObjectCollection"]["featureMember"]
        if not members: return None
        lon_str, lat_str = members[0]["GeoObject"]["Point"]["pos"].split()
        return float(lat_str), float(lon_str)
    except httpx.HTTPError:
        logger.error("Error establishing HTTP connection at the start of a geocoder call.")
        return None
    except Exception as err:
        logger.exception("Geocoding failed for address: %s", address)
        return None


async def get_coordinates(address: str, client: Optional[httpx.AsyncClient] = None) -> Optional[tuple[float, float]]:
    if client is not None:
         return await _fetch_from_geocoder(address, client)

    async with httpx.AsyncClient() as new_client:
        return await _fetch_from_geocoder(address, new_client)
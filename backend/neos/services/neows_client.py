import httpx
import os

NEOWS_FEED_URL = "https://api.nasa.gov/neo/rest/v1/feed"


class NeoWsClientError(RuntimeError):
    pass


def fetch_neows_feed(start_date, end_date, api_key=None, client=None):
    api_key = api_key or os.environ.get("NASA_API_KEY")
    
    if not api_key:
        raise NeoWsClientError("NASA_API_KEY is required")
    
    client = client or httpx.Client()

    try:
        response = client.get(
            NEOWS_FEED_URL,
            params={
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "api_key": api_key,
            },
        )
    except httpx.RequestError as exc:
        raise NeoWsClientError("NASA NeoWs request failed") from exc

    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        raise NeoWsClientError(
            f"NASA NeoWs request failed with status {exc.response.status_code}"
        ) from exc

    return response.json()
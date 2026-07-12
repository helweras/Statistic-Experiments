import httpx
from typing import Any, Dict, Optional
from config import API_PREFIX
from src.api.client import get_http_client


def post_simulate(data: Dict, endpoint):
    client = get_http_client()
    response = client.post(url=f"{API_PREFIX}{endpoint}",
                           json=data,
                           )
    response.raise_for_status()

    return response.json()["batch_results"]

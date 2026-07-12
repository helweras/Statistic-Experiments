import os
from enum import Enum

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

API_TIMEOUT_SHORT = 5.0
API_TIMEOUT_LONG = 30.0

API_PREFIX = "/api/v1"

class MontyHallEndpoints(str, Enum):
    SIMULATE = "/monty_hall/simulate"
    INFO = "/monty_hall/info"


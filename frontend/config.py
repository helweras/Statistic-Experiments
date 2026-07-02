import os
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

API_TIMEOUT_SHORT = 5.0
API_TIMEOUT_LONG = 30.0
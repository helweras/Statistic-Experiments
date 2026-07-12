import httpx
import streamlit as st
from config import BACKEND_URL

@st.cache_resource
def get_http_client() -> httpx.Client:
    # Этот клиент будет жить вечно в памяти сервера
    return httpx.Client(
        base_url=BACKEND_URL,
        timeout=20.0,
        limits=httpx.Limits(max_connections=100, max_keepalive_connections=20) # лимиты для пула
    )
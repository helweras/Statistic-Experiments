import requests
import streamlit as st
from typing import Dict, List, Optional, Union, Any


class ClientService:
    """
    Класс для выполнения сетевых запросов к API симуляции.

    Обеспечивает централизованную обработку таймаутов, ошибок сети
    и валидацию ответов сервера.
    """

    def __init__(self, base_url: str):
        """
        Args:
            base_url (str): Базовый URL сервера (напр. 'http://localhost:8000').
        """
        self.base_url = base_url.rstrip('/')

    def post_data(self, endpoint: str, payload: Dict[str, Any]) -> Optional[Union[Dict, List]]:
        """
        Отправляет POST-запрос на сервер с обработкой исключений.

        Args:
            endpoint (str): Конечная точка (напр. '/simulate').
            payload (dict): Данные для отправки в формате JSON.

        Returns:
            Optional[dict/list]: Распакованный JSON-ответ или None в случае ошибки.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        try:
            # Выполняем запрос с таймаутом (чтобы UI не завис навсегда)
            response = requests.post(url, json=payload, timeout=10)

            # Проверка статус-кодов 4xx и 5xx
            response.raise_for_status()

            return response.json()

        except requests.exceptions.Timeout:
            st.error("⌛ Превышено время ожидания ответа от сервера.")
        except requests.exceptions.ConnectionError:
            st.error("🚫 Не удалось подключиться к серверу. Проверьте, запущен ли он.")
        except requests.exceptions.HTTPError as e:
            st.error(f"❌ Ошибка сервера: {e}")
        except Exception as e:
            st.error(f"⚠️ Непредвиденная ошибка: {e}")

        return None

    @staticmethod
    def check_health(url: str) -> bool:
        """Проверяет доступность сервера (Healthcheck)."""
        try:
            return requests.get(url, timeout=2).status_code == 200
        except:
            return False

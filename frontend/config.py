import os
from src.views import monty_hall, main_page

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

API_TIMEOUT_SHORT = 5.0
API_TIMEOUT_LONG = 30.0

REGISTRY_PAGES = [
    {
        "id": "main_page",  # Технический ID (строка). Записывается в st.session_state.current_page
        "title": "Главная страница",  # Заголовок на карточке (Главная страница)
        "description": "",
        # Текст описания на карточке
        "render_func": main_page.render,  # Ссылка на функцию отрисовки самой страницы
    },

    {
        "id": "monty_hall",  # Технический ID (строка). Записывается в st.session_state.current_page
        "title": "🚪 Парадокс Монти Холла",  # Заголовок на карточке (Главная страница)
        "description": "Классическая задача теории вероятностей, основанная на американском ТВ-шоу. Узнайте, почему смена выбора двери удваивает ваши шансы на победу!",
        # Текст описания на карточке
        "render_func": monty_hall.render,  # Ссылка на функцию отрисовки самой страницы
    }
]
